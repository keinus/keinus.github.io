---
layout: default
title: Spring Security 12.3 OAuth2 Resource Server
nav_order: 1
parent: spring-security
---
                

## 12.3 OAuth 2.0 Resource Server
Spring Security는 두 가지 형태의 OAuth 2.0 베어러 토큰을 사용하여 엔드 포인트 보호를 지원합니다.

- JWT
- Opaque Tokens

응용 프로그램이 권한 관리를 권한 부여 서버 (예 : Okta 또는 Ping Identity)에 위임 한 경우에 유용합니다. 자원 서버가 이 권한 부여 서버를 참조하여 요청을 승인 할 수 있습니다.

### 12.3.1 Dependencies
대부분의 Resource Server 지원은 spring-security-oauth2-resource-server에 수집됩니다. 그러나 JWT의 디코딩 및 검증 지원은 spring-security-oauth2-jose에 있으며, 이는 JWT로 인코딩 된 베어러 토큰을 지원하는 작업 자원 서버를 갖기 위해 필요합니다.

### 12.3.2 Minimal Configuration for JWTs
Spring Boot를 사용할 때 응용 프로그램을 리소스 서버로 구성하는 것은 두 가지 기본 단계로 구성됩니다. 먼저 필요한 종속성을 포함하고 두 번째로 권한 서버의 위치를 표시하십시오.

이하 간략 정리

인증서버가 분리된 경우

```
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com/issuer
```

### 12.3.3 Specifying the Authorization Server JWK Set Uri Directly
인증서버가 리소스 서버와 동일한 경우

```
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://idp.example.com
          jwk-set-uri: https://idp.example.com/.well-known/jwks.json
```

### 12.3.4 Overriding or Replacing Boot Auto Configuration
이하 코드 기반 나머지 설정

```
protected void configure(HttpSecurity http) {
    http
        .authorizeRequests()
            .anyRequest().authenticated()
            .and()
        .oauth2ResourceServer(OAuth2ResourceServerConfigurer::jwt)
}
@EnableWebSecurity
public class MyCustomSecurityConfiguration extends WebSecurityConfigurerAdapter {
    protected void configure(HttpSecurity http) {
        http
            .authorizeRequests()
                .mvcMatchers("/messages/**").hasAuthority("SCOPE_message:read")
                .anyRequest().authenticated()
                .and()
            .oauth2ResourceServer()
                .jwt()
                    .jwtAuthenticationConverter(myConverter());
    }
}
@Bean
public JwtDecoder jwtDecoder() {
    return JwtDecoders.fromIssuerLocation(issuerUri);
}
```

jwkSetUri 설정을 코드 기반으로 할 수 있음

```
@EnableWebSecurity
public class DirectlyConfiguredJwkSetUri extends WebSecurityConfigurerAdapter {
    protected void configure(HttpSecurity http) {
        http
            .authorizeRequests()
                .anyRequest().authenticated()
                .and()
            .oauth2ResourceServer()
                .jwt()
                    .jwkSetUri("https://idp.example.com/.well-known/jwks.json");
    }
}
```

jwt 디코더 설정
```
@EnableWebSecurity
public class DirectlyConfiguredJwtDecoder extends WebSecurityConfigurerAdapter {
    protected void configure(HttpSecurity http) {
        http
            .authorizeRequests()
                .anyRequest().authenticated()
                .and()
            .oauth2ResourceServer()
                .jwt()
                    .decoder(myCustomDecoder());
    }
}
```

### 12.3.5 Configuring Trusted Algorithms
기본적으로 NimbusJwtDecoder 및 Resource Server는 RS256을 사용하는 토큰 만 신뢰하고 확인합니다.

```
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          jws-algorithm: RS512
          jwk-set-uri: https://idp.example.org/.well-known/jwks.json
```

코드로는

```
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.fromJwkSetUri(this.jwkSetUri)
            .jwsAlgorithm(RS512).build();
}
```

또는 

```
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.fromJwkSetUri(this.jwkSetUri)
            .jwsAlgorithm(RS512).jwsAlgorithm(EC512).build();
}
```

또는 

```
@Bean
JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.fromJwkSetUri(this.jwkSetUri)
            .jwsAlgorithms(algorithms -> {
                    algorithms.add(RS512);
                    algorithms.add(EC512);
            }).build();
}
```

JWK Set Uri 기반

```
@Bean
public JwtDecoder jwtDecoder() {
    // makes a request to the JWK Set endpoint
    JWSKeySelector<SecurityContext> jwsKeySelector =
            JWSAlgorithmFamilyJWSKeySelector.fromJWKSetURL(this.jwkSetUrl);

    DefaultJWTProcessor<SecurityContext> jwtProcessor =
            new DefaultJWTProcessor<>();
    jwtProcessor.setJWSKeySelector(jwsKeySelector);

    return new NimbusJwtDecoder(jwtProcessor);
}
```

### 12.3.6 Trusting a Single Asymmetric Key
JWK Set 엔드 포인트로 자원 서버를 보호하는 것보다 RSA 공개 키를 하드 코딩하는 것이 더 간단합니다. 공개 키는 Spring Boot 또는 Builder 사용을 통해 제공 될 수 있습니다.

```
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          public-key-location: classpath:my-key.pub
```

```
@Bean
BeanFactoryPostProcessor conversionServiceCustomizer() {
    return beanFactory ->
        beanFactory.getBean(RsaKeyConversionServicePostProcessor.class)
                .setResourceLoader(new CustomResourceLoader());
}
```

키 위치 설정

```
key.location: hfds://my-key.pub
```

```
@Value("${key.location}")
RSAPublicKey key;

@Bean
public JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.withPublicKey(this.key).build();
}
```

### 12.3.7 Trusting a Single Symmetric Key
대칭키도 위와 동일

```
@Bean
public JwtDecoder jwtDecoder() {
    return NimbusJwtDecoder.withSecretKey(this.key).build();
}
```

### 12.3.8 Configuring Authorization
OAuth 2.0 Authorization Server에서 발행 된 JWT는 일반적으로 scope 또는 scp 속성을 가지며, 부여 된 범위 (또는 권한)를 나타냅니다. 예를 들면 다음과 같습니다.

```
{ …​, "scope" : "messages contacts"}
```

이 경우 Resource Server는 이러한 범위를 권한이 부여 된 권한 목록으로 강제 변환하여 각 범위 앞에 문자열 "SCOPE_"를 붙입니다.
즉, JWT에서 파생 된 범위로 엔드 포인트 또는 메소드를 보호하려면 해당 표현식에 다음 접두부가 포함되어야합니다.

```
@EnableWebSecurity
public class DirectlyConfiguredJwkSetUri extends WebSecurityConfigurerAdapter {
    protected void configure(HttpSecurity http) {
        http
            .authorizeRequests(authorizeRequests -> authorizeRequests
                .mvcMatchers("/contacts/**").hasAuthority("SCOPE_contacts")
                .mvcMatchers("/messages/**").hasAuthority("SCOPE_messages")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(OAuth2ResourceServerConfigurer::jwt);
    }
}
```

또는

```
@PreAuthorize("hasAuthority('SCOPE_messages')")
public List<Message> getMessages(...) {}
```

아니면 컨버터를 사용할 수 있습니다.

```
@EnableWebSecurity
public class DirectlyConfiguredJwkSetUri extends WebSecurityConfigurerAdapter {
    protected void configure(HttpSecurity http) {
        http
            .authorizeRequests()
                .anyRequest().authenticated()
                .and()
            .oauth2ResourceServer()
                .jwt()
                    .jwtAuthenticationConverter(grantedAuthoritiesExtractor());
    }
}

Converter<Jwt, AbstractAuthenticationToken> grantedAuthoritiesExtractor() {
    JwtAuthenticationConverter jwtAuthenticationConverter = new JwtAuthenticationConverter();
    jwtAuthenticationConverter.setJwtGrantedAuthoritiesConverter(new GrantedAuthoritiesExtractor());
    return jwtAuthenticationConveter;
}
static class GrantedAuthoritiesExtractor implements Converter<Jwt, Collection<GrantedAuthority>> {

    public Collection<GrantedAuthority> convert(Jwt jwt) {
        Collection<String> authorities = (Collection<String>)jwt.getClaims().get("mycustomclaim");

        return authorities.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());
    }
}
```

### 12.3.9 Configuring Validation
timestamp 유효 검증

```
@Bean
JwtDecoder jwtDecoder() {
     NimbusJwtDecoder jwtDecoder = (NimbusJwtDecoder)
             JwtDecoders.fromIssuerLocation(issuerUri);

     OAuth2TokenValidator<Jwt> withClockSkew = new DelegatingOAuth2TokenValidator<>(
            new JwtTimestampValidator(Duration.ofSeconds(60)),
            new IssuerValidator(issuerUri));

     jwtDecoder.setJwtValidator(withClockSkew);

     return jwtDecoder;
}
```

### 12.3.10 Configuring Claim Set Mapping
생략

### 12.3.11 Configuring Timeouts
기본적으로 Resource Server는 권한 부여 서버와 조정하기 위해 각각 30 초의 연결 및 소켓 제한 시간을 사용합니다.
일부 시나리오에서는 이것이 너무 짧을 수 있습니다. 또한 백 오프 및 검색과 같은보다 정교한 패턴을 고려하지 않습니다.
리소스 서버가 인증 서버에 연결되는 방식을 조정하기 위해 NimbusJwtDecoder는 RestOperations 인스턴스를 허용합니다.

```
@Bean
public JwtDecoder jwtDecoder(RestTemplateBuilder builder) {
    RestOperations rest = builder
            .setConnectionTimeout(60000)
            .setReadTimeout(60000)
            .build();

    NimbusJwtDecoder jwtDecoder = NimbusJwtDecoder.withJwkSetUri(jwkSetUri).restOperations(rest).build();
    return jwtDecoder;
}
```

### 12.3.12 Minimal Configuration for Introspection
일반적으로 opaque 토큰은 인증 서버가 호스팅하는 OAuth 2.0 Introspection Endpoint를 통해 확인할 수 있습니다. 해지가 필요한 경우에 유용 할 수 있습니다.
Spring Boot를 사용하여 응용 프로그램을 자원 서버로 구성하는 것은 두 가지 기본 단계로 구성됩니다. 먼저 필요한 종속성을 포함시키고 두 번째로 내부 검사 엔드 포인트 세부 사항을 표시하십시오.

### Specifying the Authorization Server
내부 검사 엔드 포인트의 위치를 ​​지정하려면 다음을 수행하십시오.

```
security:
  oauth2:
    resourceserver:
      opaque-token:
        introspection-uri: https://idp.example.com/introspect
        client-id: client
        client-secret: secret
```

여기서 https://idp.example.com/introspect는 권한 부여 서버가 호스트하는 내부 검사 엔드 포인트이며 client-id 및 client-secret은 해당 엔드 포인트에 도달하는 데 필요한 자격 증명입니다.

리소스 서버는 이러한 속성을 사용하여 추가 자체 구성을 수행 한 후 들어오는 JWT를 확인합니다.





