---
layout: default
title: Spring Security OAuth2 Server
nav_order: 1
parent: spring-security
---
                

# 1. Authorization Server
Spring Security OAuth2 Boot는 OAuth 2.0 인증 서버를 간단하게 구축할 수 있습니다.

## 1.1 Do I Need to Stand Up My Own Authorization Server?
다음과 같은 경우 자체 인증 서버를 구축해야 합니다.

- 로그인, 로그 아웃 및 비밀번호 복구 작업을 자신이 관리하려는 별도의 서비스 (identity federation이라고도 함)에서 수행하려고 합니다.
- 이 별도의 서비스에 OAuth 2.0 프로토콜을 사용하여 다른 서비스와 연동하려고 합니다.

## 1.2 Dependencies
이 라이브러리에서 자동 구성 기능을 사용하려면 OAuth 2.0 기본 요소와 spring-security-oauth2-autoconfigure가있는 spring-security-oauth2가 필요합니다. spring-security-oauth2-autoconfigure 버전은 Spring Boot에서 더 이상 관리되지 않지만 Boot의 버전과 일치해야하므로 버전을 지정해야합니다.
JWT 지원을 위해서는 spring-security-jwt도 필요합니다.

## 1.3 Minimal OAuth2 Boot Configuration
최소 스프링 부트 인증 서버 생성은 다음 세 가지 기본 단계로 구성됩니다.

1. 의존성을 추가합니다.
2. @EnableAuthorizationServer 어노테이션을 추가합니다.
3. 하나 이상의 ID/PW를 입력합니다.

### 1.3.1 Enabling the Authorization Server
다른 Spring Boot @Enable 어노테이션과 유사하게 다음 예제와 같이 @EnableAuthorizationServer 어노테이션을 main 메서드가 포함 된 클래스에 추가하면 됩니다.

```
@EnableAuthorizationServer
@SpringBootApplication
public class SimpleAuthorizationServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(SimpleAuthorizationServerApplication, args);
    }
}
```

이 어노테이션을 추가하면 토큰 서명 방법, 기간 및 허용 여부와 같은 여러 가지 기본값을 가진 Spring 구성 파일을 가져옵니다.

### 1.3.2 Specifying a Client and Secret
스펙에 따라 수많은 OAuth 2.0 엔드 포인트는 클라이언트 인증이 필요하므로 권한 부여 서버와 통신 할 수 있으려면 하나 이상의 클라이언트를 지정해야합니다.
다음 예제는 클라이언트를 지정하는 방법을 보여줍니다.

```
security:
  oauth2:
    client:
      client-id: first-client
      client-secret: noonewilleverguess
```

> 편리하지만 이것은 프로덕션에서 실행 가능하지 않은 많은 가정을 만듭니다. 프로덕션으로 서비스하려면 이 이상을 수행해야합니다.

### 1.3.3 Retrieving a Token
OAuth 2.0은 기본적으로 수명이 짧은 토큰을 수명이 긴 토큰으로 교환하기 위한 전략을 지정하는 프레임워크입니다.
기본적으로 @EnableAuthorizationServer는 클라이언트 자격 증명에 대한 클라이언트 액세스 권한을 부여하므로 다음과 같은 작업을 수행 할 수 있습니다.

```
curl first-client:noonewilleverguess@localhost:8080/oauth/token -dgrant_type=client_credentials -dscope=any
```

애플리케이션은 다음과 유사한 토큰으로 응답합니다.

```
{
    "access_token" : "f05a1ea7-4c80-4583-a123-dc7a99415588",
    "token_type" : "bearer",
    "expires_in" : 43173,
    "scope" : "any"
}
```

이 토큰은 불투명 한 OAuth 2.0 토큰을 지원하는 모든 자원 서버에 제공 할 수 있으며 검증을 위해 이 권한 부여 서버를 가리 키도록 구성됩니다.

## 1.4 How to Switch Off OAuth2 Boot’s Auto Configuration
기본적으로 OAuth2 Boot 프로젝트는 기본값으로 AuthorizationServerConfigurer 인스턴스를 생성합니다.

- 이것은 NoOpPasswordEncoder를 등록합니다.(Spring Security의 기본값을 재정의함)
- 이 서버를 사용하도록 지정한 클라이언트는 이 서버가 지원하는 모든 권한 부여 유형(authorization_code, password, client_credentials, implicit 또는 refresh_token)을 사용할 수 있습니다.

또한, 생성하도록 설정(정의)된 경우 몇가지 유용한 bean을 사용할 수 있습니다.

- AuthenticationManager : 클라이언트가 아닌 최종 사용자를 찾는 경우
- TokenStore : 토큰 생성 및 검색
- AccessTokenConverter : 액세스 토큰을 JWT와 같은 다른 형식으로 변환합니다.

> 이 문서는 각 Bean이 수행하는 일부 작업만 다루고 있기 때문에, 기본 구성을 알기 위해서는 Spring Security OAuth 문서를 읽는 것이 더 좋습니다.

AuthorizationServerConfigurer 유형의 Bean을 등록하면 이 중 어느 것도 자동으로 수행되지 않습니다.
예를 들어, 둘 이상의 클라이언트를 구성하거나, 허용되는 부여 유형을 변경하거나, no-op 암호 인코더보다 더 나은 것을 사용하는 경우, (권장!) 다음과 같이 고유 한 AuthorizationServerConfigurer를 등록해야 합니다. 예는 다음과 같습니다.

```
@Configuration
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {

    @Autowired DataSource dataSource;

    protected void configure(ClientDetailsServiceConfigurer clients) {
        clients
            .jdbc(this.dataSource)
            .passwordEncoder(PasswordEncoderFactories.createDelegatingPasswordEncoder());
    }
}
```

위의 구성은 OAuth2 Boot가 더 이상 환경 특성에서 클라이언트를 검색하지 않으며, 이제 스프링 보안 비밀번호 인코더를 기본값으로 설정합니다.

## 1.5 How to Make Authorization Code Grant Flow Work
기본 구성에서는 인증 코드 흐름이 기술적으로 허용되지만 완전히 구성되지는 않습니다.
사전 구성된 기능 외에도 인증 코드 흐름에는 다음이 필요하기 때문입니다.

- 사용자
- 사용자의 로그인 flow
- 등록된 클라이언트에게 URI 재전송(redirect)

### 1.5.1 Adding End Users
Spring Security로 보안되는 일반적인 Spring Boot 애플리케이션에서 사용자는 UserDetailsService에서 정의됩니다. 이와 관련하여 다음 예제에서 보는것과 같이, 권한 부여 서버에서도 동작은 다르지 않습니다.

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean
    @Override
    public UserDetailsService userDetailsService() {
        return new InMemoryUserDetailsManager(
            User.withDefaultPasswordEncoder()
                .username("enduser")
                .password("password")
                .roles("USER")
                .build());
    }
}
```

일반적인 스프링 보안 웹 애플리케이션과 마찬가지로 사용자는 WebSecurityConfigurerAdapter 인스턴스에 정의되어 있습니다.


### 1.5.2 Adding an End-User Login Flow
또한 WebSecurityConfigurerAdapter 인스턴스를 추가하면 최종 사용자를 위한 form 로그인 플로우를 추가 할 수 있습니다. 그러나 이것은 OAuth 2.0 API가 아닌 웹 애플리케이션 자체에 관한 다른 구성이라는 점을 기억해야 합니다.
로그인 페이지를 사용자 정의하거나 사용자에게 form 로그인 이상을 제공하거나 비밀번호 복구와 같은 추가 지원을 추가하려는 경우, WebSecurityConfigurerAdapter가 이를 선택합니다.

### 1.5.3 Registering a Redirect URI With the Client
OAuth2 Boot는 client-id 및 client-secret과 함께 속성으로 리디렉션 URI 구성을 지원하지 않습니다.
리디렉션 URI를 추가하려면, InMemoryClientDetailsService 또는 JdbcClientDetailsService를 사용하여 클라이언트를 지정해야합니다.
다음 예와 같이 OAuth2 Boot에서 제공하는 AuthorizationServerConfigurer를 사용자가 구현한 구현체로 교체하는 것을 의미합니다.

```
@Configuration
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {

    @Bean
    PasswordEncoder passwordEncoder() {
        return PasswordEncoderFactories.createDelegatingPasswordEncoder();
    }

    protected void configure(ClientDetailsServiceConfigurer clients) {
        clients
            .inMemory()
                .withClient("first-client")
                .secret(passwordEncoder().encode("noonewilleverguess"))
                .scopes("resource:read")
                .authorizedGrantTypes("authorization_code")
                .redirectUris("http://localhost:8081/oauth/login/client-app");
    }
}
```

### 1.5.4 Testing Authorization Code Flow
전체 흐름을 보려면 서버가 두 대 이상 필요하기 때문에 OAuth 테스트가 까다로울 수 있습니다. 그러나 첫 단계는 간단합니다.

1. http://localhost:8080/oauth/authorize?grant_type=authorization_code&response_type=code&client_id=first-client&state=1234
2. 로그인되어 있지 않은 사용자의 경우, 애플리케이션은 로그인 페이지(http://localhost:8080/login)로 리디렉션됩니다.
3. 사용자가 로그인하면 애플리케이션이 코드를 생성하고 등록 된 리디렉션 URI(http://localhost:8081/oauth/login/client-app)로 리디렉션합니다.

이 시점에서 불투명 토큰에 대해 구성되고 이 권한 부여 서버 인스턴스를 가리키는 모든 자원 서버를 구축하여 플로우를 계속할 수 있습니다.


## 1.6 How to Make Password Grant Flow Work
기본 구성을 사용하면 암호 흐름이 기술적으로 가능하지만 인증 코드와 같이 사용자가 누락됩니다.
즉, 기본 구성은 사용자 이름이 user이고 임의로 생성 된 비밀번호를 사용하여 사용자를 작성하므로, 가상적으로 로그의 비밀번호를 확인할 수 있으며, 다음을 수행 할 수 있습니다.

```
curl first-client:noonewilleverguess@localhost:8080/oauth/token -dgrant_type=password -dscope=any -dusername=user -dpassword=the-password-from-the-logs
```

해당 명령을 실행할 때 토큰을 다시 가져와야합니다.
그러나 사용자 리스트를 생성하려고 합니다.
스프링 보안에서 1.5 절.“권한 부여 코드 부여 흐름을 작동시키는 방법”에 언급 된 것처럼, 사용자는 일반적으로 UserDetailsService에서 생성되며 다음 예제와 같이 이 응용 프로그램 또한 다르지 않습니다.

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean
    @Override
    public UserDetailsService userDetailsService() {
        return new InMemoryUserDetailsManager(
            User.withDefaultPasswordEncoder()
                .username("enduser")
                .password("password")
                .roles("USER")
                .build());
    }
}
```

이것이 우리가해야 할 전부입니다. 클라이언트 ID 및 비밀번호가 환경 설정값으로 지정되므로 AuthorizationServerConfigurer를 재정의할 필요가 없습니다.
이제 다음이 작동합니다.

```
curl first-client:noonewilleverguess@localhost:8080/oauth/token -dgrant_type=password -dscope=any -dusername=enduser -dpassword=password

```

## 1.7 How and When to Give Authorization Server an AuthenticationManager
AuthorizationServerEndpointsConfigurer에 AuthenticationManager 인스턴스를 언제 지정해야하는지 물어보는 것은 매우 일반적인 질문이면서도, 매우 직관적이지 않습니다. 질문에 대한 대답은 다음과 같습니다. Resource Owner Password Flow를 사용하는 경우에만 해당됩니다.
다음은 몇 가지 기본 사항을 기억하는데 도움이됩니다.

- AuthenticationManager는 사용자 인증을 위한 추상화입니다. 일반적으로 인증을 완료하려면 UserDetailsService나 재정의된 서비스를 지정해야합니다.
- 최종 사용자는 WebSecurityConfigurerAdapter에 지정되어 있습니다.
- OAuth2 Boot는 기본적으로 노출 된 AuthenticationManager를 자동으로 선택합니다.

그러나 모든 흐름에 최종 사용자가 포함되는 것은 아니기 때문에, 모든 흐름에 AuthenticationManager가 필요한 것은 아닙니다. 예를 들어, 클라이언트 자격 증명 흐름은 최종 사용자의 권한이 아닌 클라이언트의 권한만을 사용하여 토큰을 요청합니다. Refresh 토큰 흐름은 Refresh 토큰의 권한만으로 토큰을 요청합니다.
또한 모든 흐름에 OAuth 2.0 API 자체에 AuthenticationManager가 있어야하는 것은 아닙니다. 예를 들어, Authorization Code 및 암시적 흐름은 토큰 (OAuth 2.0 API)이 요청 될 때가 아니라 로그인 할 때 (응용 프로그램 흐름) 사용자를 확인합니다.
Resource Owner Password 흐름만 최종 사용자의 자격 증명을 기반으로 코드를 반환합니다. 이는 클라이언트가 Resource Owner Password 플로우를 사용하는 경우 권한 부여 서버에만 AuthenticationManager가 필요함을 의미합니다.
다음 예는 Resource Owner Password 플로우를 보여줍니다.

```
.authorizedGrantTypes("password", ...)
```

이전 흐름에서 Authorization Server는 AuthenticationManager 인스턴스가 필요했었습니다.
이를 수행하는 몇 가지 방법이 있습니다.

- OAuth2 부팅 기본값을 유지하고 (AuthorizationServerConfigurer를 등록하지 않음) UserDetailsService를 등록하십시오.
- OAuth2 Boot 기본값을 그대로두고 AuthenticationManager를 등록하십시오.
- AuthorizationServerConfigurerAdapter 재정의하세요.(기본값 삭제) 그리고 AuthenticationConfiguration에 의존하세요.
- AuthorizationServerConfigurerAdapter를 재정의하고 AuthenticationManager를 수동으로 연결하십시오.

### 1.7.1 Exposing a UserDetailsService
최종 사용자는 UserDetailsService를 통해 WebSecurityConfigurerAdapter에 지정됩니다. 따라서 OAuth2 Boot 기본값을 사용하는 경우 (AuthorizationServerConfigurer를 구현하지 않았다는 의미) 다음 예제와 같이 UserDetailsService를 등록하는 것으로 끝낼 수 있습니다.

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Autowired DataSource dataSource;

    @Bean
    @Override
    public UserDetailsService userDetailsService() {
        return new JdbcUserDetailsManager(this.dataSource);
    }
}
```

### 1.7.2 Exposing an AuthenticationManager
보다 전문화 된 AuthenticationManager 구성이 필요한 경우, WebSecurityConfigurerAdapter에서 구성한 후 다음 예제와 같이 이를 등록 할 수 있습니다.

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean(BeansId.AUTHENTICATION_MANAGER)
    @Override
    public AuthenticationManager authenticationManagerBean() {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(customAuthenticationProvider());
    }
}
```

### 1.7.3 Depending on AuthenticationConfiguration
구성된 AuthenticationManager는 AuthenticationConfiguration에서 사용할 수 있습니다. 즉, AuthorizationServerConfigurer가 필요한 경우 (개발자가 autowiring을 수행해야하는 경우) 다음 클래스와 같이 AuthenticationConfiguration Bean을 가져 오기 위해 AuthenticationConfiguration에 의존할 수 있습니다.

```
@Component
public class CustomAuthorizationServerConfigurer extends
    AuthorizationServerConfigurerAdapter {

    AuthenticationManager authenticationManager;

    public CustomAuthorizationServerConfigurer(AuthenticationConfiguration authenticationConfiguration) {
        this.authenticationManager = authenticationConfiguration.getAuthenticationManager();
    }

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) {
        // .. your client configuration that allows the password grant
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }
}
```

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean
    @Override
    public UserDetailsService userDetailsService() {
        return new MyCustomUserDetailsService();
    }
}
```

### 1.7.4 Manually Wiring An AuthenticationManager
AuthenticationManager에 특수한 구성이 필요하고, 고유한 AuthenticationServerConfigurer가 있는 가장 복잡한 케이스의 경우, 고유한 AuthorizationServerConfigurerAdapter와 고유한 WebSecurityConfigurerAdapter를 작성해야합니다.

```
@Component
public class CustomAuthorizationServerConfigurer extends
    AuthorizationServerConfigurerAdapter {

    AuthenticationManager authenticationManager;

    public CustomAuthorizationServerConfigurer(AuthenticationManager authenticationManager) {
        this.authenticationManager = authenticationManager;
    }

    @Override
    public void configure(ClientDetailsServiceConfigurer clients) {
        // .. your client configuration that allows the password grant
    }

    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
        endpoints.authenticationManager(authenticationManager);
    }
}
```

```
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    @Bean(BeansId.AUTHENTICATION_MANAGER)
    @Override
    public AuthenticationManager authenticationManagerBean() {
        return super.authenticationManagerBean();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) {
        auth.authenticationProvider(customAuthenticationProvider());
    }
}
```

### 1.8 Is Authorization Server Compatible with Spring Security 5.1 Resource Server and Client?
아닙니다. Spring Security 5.1은 JWT로 인코딩된 JWK-signed 인증만 지원하며, Authorization Server는 JWK Set URI와 함께 제공되지 않습니다.
그래도 기본적인 지원은 가능합니다.
예를 들어 Authorization Server가 Spring Security 5.1 Resource Server와 호환되도록 구성하려면 다음을 수행해야합니다.

### 1.8.1 Configuring Authorization Server to Use JWKs
액세스 및 새로 고침 토큰에 사용되는 형식을 변경하려면 다음 예제와 같이 AccessTokenConverter 및 TokenStore를 변경하십시오.

```
@EnableAuthorizationServer
@Configuration
public class JwkSetConfiguration extends AuthorizationServerConfigurerAdapter {

	AuthenticationManager authenticationManager;
	KeyPair keyPair;

	public JwkSetConfiguration(AuthenticationConfiguration authenticationConfiguration,
			KeyPair keyPair) throws Exception {

		this.authenticationManager = authenticationConfiguration.getAuthenticationManager();
		this.keyPair = keyPair;
	}

    // ... client configuration, etc.

	@Override
	public void configure(AuthorizationServerEndpointsConfigurer endpoints) {
		// @formatter:off
		endpoints
			.authenticationManager(this.authenticationManager)
			.accessTokenConverter(accessTokenConverter())
			.tokenStore(tokenStore());
		// @formatter:on
	}

	@Bean
	public TokenStore tokenStore() {
		return new JwtTokenStore(accessTokenConverter());
	}

	@Bean
	public JwtAccessTokenConverter accessTokenConverter() {
		JwtAccessTokenConverter converter = new JwtAccessTokenConverter();
		converter.setKeyPair(this.keyPair);
		return converter;
	}
}
```

### 1.8.2 Add a JWK Set URI Endpoint
Spring Security OAuth는 JWK를 지원하지 않으며 @EnableAuthorizationServer는 초기 세트에 더 많은 OAuth 2.0 API 엔드 포인트 추가를 지원하지 않습니다. 그러나 몇 줄만 추가하면됩니다. 
먼저 com.nimbusds : nimbus-jose-jwt와 같은 다른 종속성을 추가해야합니다. 이것은 적절한 JWK 프리미티브를 제공합니다. 
둘째, @EnableAuthorizationServer를 사용하는 대신 두 개의 @Configuration 클래스를 직접 포함시켜야합니다.

- AuthorizationServerEndpointsConfiguration : 토큰에 사용할 형식과 같은 OAuth 2.0 API 엔드 포인트를 구성하기위한 @Configuration 클래스.
- AuthorizationServerSecurityConfiguration : 엔드 포인트 주변의 액세스 규칙에 대한 @Configuration 클래스. 다음 예제와 같이 확장해야합니다.

```
@FrameworkEndpoint
class JwkSetEndpoint {
	KeyPair keyPair;

	public JwkSetEndpoint(KeyPair keyPair) {
		this.keyPair = keyPair;
	}

	@GetMapping("/.well-known/jwks.json")
	@ResponseBody
	public Map<String, Object> getKey(Principal principal) {
		RSAPublicKey publicKey = (RSAPublicKey) this.keyPair.getPublic();
		RSAKey key = new RSAKey.Builder(publicKey).build();
		return new JWKSet(key).toJSONObject();
	}
}
```

```
@Configuration
class JwkSetEndpointConfiguration extends AuthorizationServerSecurityConfiguration {
	@Override
	protected void configure(HttpSecurity http) throws Exception {
		super.configure(http);
		http
			.requestMatchers()
				.mvcMatchers("/.well-known/jwks.json")
				.and()
			.authorizeRequests()
				.mvcMatchers("/.well-known/jwks.json").permitAll();
	}
}
```

그런 다음 AuthorizationServerEndpointsConfiguration을 변경할 필요가 없으므로 다음 예제와 같이 @EnableAuthorizationServer를 사용하는 대신 @Import 가져 오기를 수행 할 수 있습니다.

```
@Import(AuthorizationServerEndpointsConfiguration.class)
@Configuration
public class JwkSetConfiguration extends AuthorizationServerConfigurerAdapter {

    // ... the rest of the configuration from the previous section
}
```

### 1.8.3 Testing Against Spring Security 5.1 Resource Server
이제 / oauth / token 엔드 포인트에 POST하여 (이전과 같이) 토큰을 얻은 다음이를 스프링 보안 5.1 리소스 서버에 제공 할 수 있습니다.
