---
layout: default
title: Spring Security 12. Oauth2
nav_order: 1
parent: spring-security
---
                

# 12. OAuth2
## 12.1 OAuth 2.0 Login
OAuth 2.0 로그인 기능은 사용자가 OAuth 2.0 제공자 (예 : GitHub) 또는 OpenID Connect 1.0 제공자 (예 : Google)에 등록된 계정을 사용하여 애플리케이션에 로그인할 수 있는 기능을 제공합니다. OAuth 2.0 로그인은 "Google로 로그인"또는 "GitHub로 로그인" 사용 사례를 구현합니다.

> OAuth 2.0 로그인은 OAuth 2.0 인증 프레임 워크 및 OpenID Connect Core 1.0에 지정된 Authorization Code Grant를 사용하여 구현됩니다.

### 12.1.1 Spring Boot 2.x Sample
Spring Boot 2.x는 OAuth 2.0 로그인을위한 완전한 자동 구성 기능을 제공합니다.
이 섹션에서는 Google을 인증 공급자로 사용하여 OAuth 2.0 로그인 샘플을 구성하는 방법을 보여주고 다음 주제를 다룹니다.

### Initial setup
로그인에 Google OAuth 2.0 인증 시스템을 사용하려면 Google API 콘솔에서 OAuth 2.0 자격 증명을 얻도록 프로젝트를 설정해야합니다.

> 인증을위한 Google의 OAuth 2.0 구현은 OpenID Connect 1.0 사양을 준수하며 OpenID 인증을 받았습니다.

"OAuth 2.0 설정"섹션에서 시작하여 OpenID Connect 페이지의 지시 사항을 따르십시오.
"OAuth 2.0 자격 증명 얻기"지침을 완료 한 후에는 클라이언트 ID와 클라이언트 암호로 구성된 자격 증명이있는 새 OAuth 클라이언트가 있어야합니다.

### Setting the redirect URI
리디렉션 URI는 최종 사용자의 사용자 에이전트가 Google에서 인증 한 후 동의 페이지의 OAuth 클라이언트 (이전 단계에서 생성)에 대한 액세스 권한을 부여한 후 다시 리디렉션되는 애플리케이션의 경로입니다.
"리디렉션 URI 설정"하위 섹션에서 승인 된 리디렉션 URI 필드가 http://localhost:8080/login/oauth2/code/google로 설정되어 있는지 확인하십시오.

> 기본 경로 재 지정 URI 템플리트는 {baseUrl}/login/oauth2/code/{registrationId}입니다. registrationId는 ClientRegistration의 고유 식별자입니다.

> OAuth 클라이언트가 프록시 서버 뒤에서 실행 중인 경우 프록시 서버 구성을 확인하여 응용 프로그램이 올바르게 구성되어 있는지 확인하는 것이 좋습니다. 또한 redirect-uri에 대해 지원되는 URI 템플릿 변수를 참조하십시오.

### Configure application.yml
Google에 새로운 OAuth 클라이언트가 생겼으므로 인증 흐름에 OAuth 클라이언트를 사용하도록 애플리케이션을 구성해야합니다. 그렇게하려면 :

먼저 application.yml로 이동하여 다음 구성을 설정하십시오.

```
spring:
  security:
    oauth2:
      client:
        registration:   1
          google:   2
            client-id: google-client-id
            client-secret: google-client-secret
```

**Example 12.1. OAuth Client properties**
1. spring.security.oauth2.client.registration은 OAuth 클라이언트 속성의 기본 속성 접두사입니다.
2. 기본 속성 접두사 뒤에는 Google과 같은 ClientRegistration의 ID가 있습니다.

그 다음, client-id 및 client-secret 특성의 값을 이전에 작성한 OAuth 2.0 credentials 정보로 바꾸십시오.

### Boot up the application
Spring Boot 2.x 샘플을 시작하고 http://localhost:8080으로 이동하십시오. 그런 다음 Google에 대한 링크를 표시하는 기본 자동 생성 로그인 페이지로 리디렉션됩니다.
Google 링크를 클릭하면 인증을 위해 Google로 리디렉션됩니다.
Google 계정 자격 증명으로 인증 한 후 다음 페이지는 동의 화면입니다. 동의 화면에 앞서 생성 한 OAuth 클라이언트에 대한 액세스를 허용 또는 거부하도록 요청합니다. 허용을 클릭하면 OAuth 클라이언트가 이메일 주소 및 기본 프로필 정보에 액세스 할 수있는 권한을 부여합니다.
이 시점에서 OAuth 클라이언트는 UserInfo Endpoint에서 이메일 주소와 기본 프로필 정보를 검색하고 인증 된 세션을 설정합니다.

### 12.1.2 Spring Boot 2.x Property Mappings
다음 표는 Spring Boot 2.x OAuth 클라이언트 특성과 ClientRegistration 특성의 맵핑을 간략하게 설명합니다.

| Spring Boot 2.x	                                                                   | ClientRegistration                              |
| ---------------------------------------------------------------------------------------- | ---------------------------------- |
| spring.security.oauth2.client.registration.[registrationId]                              | registrationId |
| spring.security.oauth2.client.registration.[registrationId].client-id | clientId |
| spring.security.oauth2.client.registration.[registrationId].client-secret | clientSecret |
| spring.security.oauth2.client.registration.[registrationId].client-authentication-method | clientAuthenticationMethod |
| spring.security.oauth2.client.registration.[registrationId].authorization-grant-type | authorizationGrantType |
| spring.security.oauth2.client.registration.[registrationId].redirect-uri | redirectUriTemplate |
| spring.security.oauth2.client.registration.[registrationId].scope | scopes |
| spring.security.oauth2.client.registration.[registrationId].client-name | clientName |
| spring.security.oauth2.client.provider.[providerId].authorization-uri | providerDetails.authorizationUri |
| spring.security.oauth2.client.provider.[providerId].token-uri | providerDetails.tokenUri |
| spring.security.oauth2.client.provider.[providerId].jwk-set-uri | providerDetails.jwkSetUri |
| spring.security.oauth2.client.provider.[providerId].user-info-uri | providerDetails.userInfoEndpoint.uri |
| spring.security.oauth2.client.provider.[providerId].user-info-authentication-method | providerDetails.userInfoEndpoint.authenticationMethod |
| spring.security.oauth2.client.provider.[providerId].userNameAttribute | providerDetails.userInfoEndpoint.userNameAttributeName |

> spring.security.oauth2.client.provider. [providerId] .issuer-uri 특성을 지정하여 OpenID Connect 제공자의 구성 엔드 포인트 또는 권한 부여 서버의 메타 데이터 엔드 포인트 발견을 사용하여 ClientRegistration을 초기에 구성 할 수 있습니다.

### 12.1.3 CommonOAuth2Provider
CommonOAuth2Provider는 잘 알려진 여러 제공자 (Google, GitHub, Facebook 및 Okta)에 대한 기본 클라이언트 특성 세트를 사전 정의합니다.
예를 들어, authorization-uri, token-uri 및 user-info-uri는 제공자에 대해 자주 변경되지 않습니다. 따라서 필요한 구성을 줄이려면 기본값을 제공하는 것이 좋습니다.
앞에서 설명한 것처럼 Google 클라이언트를 구성 할 때 client-id 및 client-secret 속성 만 필요합니다.
다음 목록은 예입니다.

```
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: google-client-id
            client-secret: google-client-secret
```

> registrationId (google)가 CommonOAuth2Provider의 GOOGLE 열거 형 (대 / 소문자 구분 안 함)과 일치하기 때문에 클라이언트 속성의 자동 기본 설정이 완벽하게 작동합니다.

google-login과 같은 다른 registrationId를 지정하려는 경우에도 제공자 특성을 구성하여 클라이언트 특성의 자동 기본값을 활용할 수 있습니다.
다음 목록은 예입니다.

```
spring:
  security:
    oauth2:
      client:
        registration:
          google-login: 1
            provider: google    2
            client-id: google-client-id
            client-secret: google-client-secret
```

1. registrationId가 google-login으로 설정되어 있습니다.
2. 공급자 속성은 google로 설정되며 CommonOAuth2Provider.GOOGLE.getBuilder ()에 설정된 클라이언트 속성의 자동 기본값을 활용합니다.

### 12.1.4 Configuring Custom Provider Properties
다중 테넌시를 지원하는 일부 OAuth 2.0 제공자가 있으므로 각 테넌트 (또는 하위 도메인)마다 다른 프로토콜 엔드 포인트가 발생합니다.
예를 들어 Okta에 등록 된 OAuth 클라이언트는 특정 하위 도메인에 할당되고 고유 한 프로토콜 엔드 포인트가 있습니다.
이러한 경우 Spring Boot 2.x는 사용자 정의 제공자 특성을 구성하기위한 다음 기본 특성을 제공합니다. spring.security.oauth2.client.provider. [providerId].
다음 목록은 예입니다.

```
spring:
  security:
    oauth2:
      client:
        registration:
          okta:
            client-id: okta-client-id
            client-secret: okta-client-secret
        provider:
          okta: 1
            authorization-uri: https://your-subdomain.oktapreview.com/oauth2/v1/authorize
            token-uri: https://your-subdomain.oktapreview.com/oauth2/v1/token
            user-info-uri: https://your-subdomain.oktapreview.com/oauth2/v1/userinfo
            user-name-attribute: sub
            jwk-set-uri: https://your-subdomain.oktapreview.com/oauth2/v1/keys
```

1. 기본 속성 (spring.security.oauth2.client.provider.okta)을 사용하면 프로토콜 엔드 포인트 위치를 사용자 정의 할 수 있습니다.

### 12.1.5 Overriding Spring Boot 2.x Auto-configuration
OAuth 클라이언트 지원을위한 Spring Boot 2.x 자동 구성 클래스는 OAuth2ClientAutoConfiguration입니다.
다음 작업을 수행합니다.

- 구성된 OAuth 클라이언트 특성에서 ClientRegistration으로 구성된 ClientRegistrationRepository @Bean을 등록합니다.
- WebSecurityConfigurerAdapter @Configuration을 제공하고 httpSecurity.oauth2Login()을 통해 OAuth 2.0 로그인을 활성화합니다.

특정 요구 사항에 따라 자동 구성을 재정의해야하는 경우 다음과 같은 방법으로 수행 할 수 있습니다.

### Register a ClientRegistrationRepository @Bean
다음 예제는 ClientRegistrationRepository @Bean을 등록하는 방법을 보여줍니다.

```
@Configuration
public class OAuth2LoginConfig {

    @Bean
    public ClientRegistrationRepository clientRegistrationRepository() {
        return new InMemoryClientRegistrationRepository(this.googleClientRegistration());
    }

    private ClientRegistration googleClientRegistration() {
        return ClientRegistration.withRegistrationId("google")
            .clientId("google-client-id")
            .clientSecret("google-client-secret")
            .clientAuthenticationMethod(ClientAuthenticationMethod.BASIC)
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .redirectUriTemplate("{baseUrl}/login/oauth2/code/{registrationId}")
            .scope("openid", "profile", "email", "address", "phone")
            .authorizationUri("https://accounts.google.com/o/oauth2/v2/auth")
            .tokenUri("https://www.googleapis.com/oauth2/v4/token")
            .userInfoUri("https://www.googleapis.com/oauth2/v3/userinfo")
            .userNameAttributeName(IdTokenClaimNames.SUB)
            .jwkSetUri("https://www.googleapis.com/oauth2/v3/certs")
            .clientName("Google")
            .build();
    }
}
```

### Provide a WebSecurityConfigurerAdapter
다음 예제는 @EnableWebSecurity를 ​​WebSecurityConfigurerAdapter에 제공하고 httpSecurity.oauth2Login()을 통해 OAuth 2.0 로그인을 사용하는 방법을 보여줍니다.

```
@Configuration
public class OAuth2LoginConfig {

    @EnableWebSecurity
    public static class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                .authorizeRequests(authorizeRequests ->
                    authorizeRequests
                        .anyRequest().authenticated()
                )
                .oauth2Login(withDefaults());
        }
    }

    @Bean
    public ClientRegistrationRepository clientRegistrationRepository() {
        return new InMemoryClientRegistrationRepository(this.googleClientRegistration());
    }

    private ClientRegistration googleClientRegistration() {
        return ClientRegistration.withRegistrationId("google")
            .clientId("google-client-id")
            .clientSecret("google-client-secret")
            .clientAuthenticationMethod(ClientAuthenticationMethod.BASIC)
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .redirectUriTemplate("{baseUrl}/login/oauth2/code/{registrationId}")
            .scope("openid", "profile", "email", "address", "phone")
            .authorizationUri("https://accounts.google.com/o/oauth2/v2/auth")
            .tokenUri("https://www.googleapis.com/oauth2/v4/token")
            .userInfoUri("https://www.googleapis.com/oauth2/v3/userinfo")
            .userNameAttributeName(IdTokenClaimNames.SUB)
            .jwkSetUri("https://www.googleapis.com/oauth2/v3/certs")
            .clientName("Google")
            .build();
    }
}
```

### 12.1.6 Java Configuration without Spring Boot 2.x
Spring Boot 2.x를 사용할 수없고 CommonOAuth2Provider에서 사전 정의 된 제공자 중 하나를 구성하려면 (예 : Google) 다음 구성을 적용하십시오.

```
@Configuration
public class OAuth2LoginConfig {

    @EnableWebSecurity
    public static class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                .authorizeRequests(authorizeRequests ->
                    authorizeRequests
                        .anyRequest().authenticated()
                )
                .oauth2Login(withDefaults());
        }
    }

    @Bean
    public ClientRegistrationRepository clientRegistrationRepository() {
        return new InMemoryClientRegistrationRepository(this.googleClientRegistration());
    }

    @Bean
    public OAuth2AuthorizedClientService authorizedClientService(
            ClientRegistrationRepository clientRegistrationRepository) {
        return new InMemoryOAuth2AuthorizedClientService(clientRegistrationRepository);
    }

    @Bean
    public OAuth2AuthorizedClientRepository authorizedClientRepository(
            OAuth2AuthorizedClientService authorizedClientService) {
        return new AuthenticatedPrincipalOAuth2AuthorizedClientRepository(authorizedClientService);
    }

    private ClientRegistration googleClientRegistration() {
        return CommonOAuth2Provider.GOOGLE.getBuilder("google")
            .clientId("google-client-id")
            .clientSecret("google-client-secret")
            .build();
    }
}
```

### 12.1.7 Advanced Configuration
HttpSecurity.oauth2Login()은 OAuth 2.0 로그인을 사용자 정의하기 위한 여러 구성 옵션을 제공합니다. 기본 구성 옵션은 프로토콜 엔드 포인트 대응으로 그룹화됩니다.
예를 들어, oauth2Login().authorizationEndpoint()는 권한 부여 엔드 포인트 구성을 허용하고, oauth2Login().tokenEndpoint()는 토큰 엔드 포인트 구성을 허용합니다.
다음 코드는 예를 보여줍니다.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .authorizationEndpoint(authorizationEndpoint ->
                        authorizationEndpoint
                            ...
                    )
                    .redirectionEndpoint(redirectionEndpoint ->
                        redirectionEndpoint
                            ...
                    )
                    .tokenEndpoint(tokenEndpoint ->
                        tokenEndpoint
                            ...
                    )
                    .userInfoEndpoint(userInfoEndpoint ->
                        userInfoEndpoint
                            ...
                    )
            );
    }
}
```

oauth2Login() DSL의 주요 목표는 사양에 정의 된대로 이름과 밀접하게 일치하는 것이 었습니다.
OAuth 2.0 인증 프레임 워크는 다음과 같이 프로토콜 엔드 포인트를 정의합니다.
권한 부여 프로세스는 두 개의 권한 부여 서버 엔드 포인트 (HTTP 자원)를 사용합니다.

- 권한 부여 엔드포인트 : 클라이언트가 사용자 에이전트 리디렉션을 통해 리소스 소유자로부터 권한을 얻기 위해 사용합니다.
- 토큰 엔드 포인트 : 클라이언트가 일반적으로 클라이언트 인증을 사용하여 액세스 토큰에 대한 권한 부여를 교환하기 위해 사용합니다.

하나의 클라이언트 엔드 포인트는 물론 :

- 리디렉션 엔드포인트 : 권한 부여 서버가 리소스 소유자 user-agent를 통해 권한 부여 자격 증명이 포함 된 응답을 클라이언트에 반환하는 데 사용됩니다.

OpenID Connect Core 1.0 사양은 다음과 같이 UserInfo Endpoint를 정의합니다.
UserInfo Endpoint는 인증 된 최종 사용자에 대한 클레임을 반환하는 OAuth 2.0 보호 리소스입니다. 최종 사용자에 대한 요청 된 클레임을 얻기 위해 클라이언트는 OpenID Connect 인증을 통해 얻은 액세스 토큰을 사용하여 UserInfo Endpoint에 요청합니다. 이러한 클레임은 일반적으로 클레임의 이름-값 쌍 모음을 포함하는 JSON 객체로 표시됩니다.
다음 코드는 oauth2Login() DSL에 사용 가능한 전체 구성 옵션을 보여줍니다.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .clientRegistrationRepository(this.clientRegistrationRepository())
                    .authorizedClientRepository(this.authorizedClientRepository())
                    .authorizedClientService(this.authorizedClientService())
                    .loginPage("/login")
                    .authorizationEndpoint(authorizationEndpoint ->
                        authorizationEndpoint
                            .baseUri(this.authorizationRequestBaseUri())
                            .authorizationRequestRepository(this.authorizationRequestRepository())
                            .authorizationRequestResolver(this.authorizationRequestResolver())
                    )
                    .redirectionEndpoint(redirectionEndpoint ->
                         redirectionEndpoint
                            .baseUri(this.authorizationResponseBaseUri())
                    )
                    .tokenEndpoint(tokenEndpoint ->
                        tokenEndpoint
                            .accessTokenResponseClient(this.accessTokenResponseClient())
                    )
                    .userInfoEndpoint(userInfoEndpoint ->
                        userInfoEndpoint
                            .userAuthoritiesMapper(this.userAuthoritiesMapper())
                            .userService(this.oauth2UserService())
                            .oidcUserService(this.oidcUserService())
                            .customUserType(GitHubOAuth2User.class, "github")
                    )
            );
    }
}
```

다음 섹션에서는 사용 가능한 각 구성 옵션에 대해 자세히 설명합니다.

### OAuth 2.0 Login Page
기본적으로 OAuth 2.0 로그인 페이지는 DefaultLoginPageGeneratingFilter에 의해 자동 생성됩니다. 기본 로그인 페이지에는 ClientRegistration.clientName을 사용하여 구성된 각 OAuth 클라이언트가 링크로 표시되어 권한 부여 요청 (또는 OAuth 2.0 로그인)을 시작할 수 있습니다.

> DefaultLoginPageGeneratingFilter가 구성된 OAuth 클라이언트에 대한 링크를 표시하려면 등록 된 ClientRegistrationRepository도 Iterable <ClientRegistration>을 구현해야합니다. 참조는 InMemoryClientRegistrationRepository를 참조하십시오.

각 OAuth 클라이언트의 링크 대상은 기본적으로 다음과 같습니다.

```
OAuth2AuthorizationRequestRedirectFilter.DEFAULT_AUTHORIZATION_REQUEST_BASE_URI + "/{registrationId}"
```

다음 줄은 예를 보여줍니다.

```
<a href="/oauth2/authorization/google">Google</a>
```

기본 로그인 페이지를 대체하려면 oauth2Login().loginPage() 및 (선택적으로) oauth2Login().authorizationEndpoint().baseUri()를 구성하십시오.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .loginPage("/login/oauth2")
                    ...
                    .authorizationEndpoint(authorizationEndpoint ->
                        authorizationEndpoint
                            .baseUri("/login/oauth2/authorization")
                            ...
                    )
            );
    }
}
```

> 사용자 정의 로그인 페이지를 렌더링 할 수있는 @RequestMapping("/login/oauth2")을 @Controller에 제공해야합니다.

> 앞에서 언급했듯이 oauth2Login (). authorizationEndpoint (). baseUri () 구성은 선택 사항입니다. 그러나 사용자 정의하도록 선택한 경우 각 OAuth 클라이언트에 대한 링크가 authorizationEndpoint (). baseUri ()와 일치하는지 확인하십시오. `<a href="/login/oauth2/authorization/google">Google</a>`

### Redirection Endpoint
리디렉션 엔드포인트는 권한 부여 서버에서 리소스 소유자 사용자 에이전트를 통해 권한 부여 자격 증명이 포함 된 권한 부여 응답을 클라이언트에 반환하기 위해 사용됩니다.

> OAuth 2.0 로그인은 인증 코드 부여를 활용합니다. 따라서 권한 정보는 권한 코드입니다.

기본 권한 부여 응답 baseUri (리디렉션 엔드 포인트)는 /login/oauth2/code/*이며 OAuth2LoginAuthenticationFilter.DEFAULT_FILTER_PROCESSES_URI에 정의되어 있습니다.
권한 부여 응답 baseUri를 사용자 정의하려면 다음 예제와 같이 구성하십시오.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .redirectionEndpoint(redirectionEndpoint ->
                        redirectionEndpoint
                            .baseUri("/login/oauth2/callback/*")
                            ...
                    )
            );
    }
}
```

> 또한 ClientRegistration.redirectUriTemplate이 사용자 정의 권한 부여 응답 baseUri와 일치하는지 확인해야합니다.
```
return CommonOAuth2Provider.GOOGLE.getBuilder("google")
    .clientId("google-client-id")
    .clientSecret("google-client-secret")
    .redirectUriTemplate("{baseUrl}/login/oauth2/callback/{registrationId}")
    .build();
```

### UserInfo Endpoint
UserInfo 엔드 포인트에는 다음 하위 섹션에 설명 된대로 여러 구성 옵션이 포함되어 있습니다.

- Mapping User Authorities
- Configuring a Custom OAuth2User
- OAuth 2.0 UserService
- OpenID Connect 1.0 UserService

### Mapping User Authorities
사용자가 OAuth 2.0 제공자로 인증 한 후 OAuth2User.getAuthorities() (또는 OidcUser.getAuthorities())는 새로운 GrantedAuthority 인스턴스 세트에 맵핑 될 수 있으며, 인증이 완료되면 OAuth2AuthenticationToken으로 제공됩니다.

> OAuth2AuthenticationToken.getAuthorities()는 hasRole('USER') 또는 hasRole('ADMIN')과 같은 요청을 승인하는 데 사용됩니다.

사용자 권한을 맵핑 할 때 선택할 수있는 몇 가지 옵션이 있습니다.

- Using a GrantedAuthoritiesMapper
- Delegation-based strategy with OAuth2UserService

### Using a GrantedAuthoritiesMapper
GrantedAuthoritiesMapper의 구현을 제공하고 다음 예제와 같이 구성하십시오.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .userInfoEndpoint(userInfoEndpoint ->
                        userInfoEndpoint
                            .userAuthoritiesMapper(this.userAuthoritiesMapper())
                            ...
                    )
            );
    }

    private GrantedAuthoritiesMapper userAuthoritiesMapper() {
        return (authorities) -> {
            Set<GrantedAuthority> mappedAuthorities = new HashSet<>();

            authorities.forEach(authority -> {
                if (OidcUserAuthority.class.isInstance(authority)) {
                    OidcUserAuthority oidcUserAuthority = (OidcUserAuthority)authority;

                    OidcIdToken idToken = oidcUserAuthority.getIdToken();
                    OidcUserInfo userInfo = oidcUserAuthority.getUserInfo();

                    // Map the claims found in idToken and/or userInfo
                    // to one or more GrantedAuthority's and add it to mappedAuthorities

                } else if (OAuth2UserAuthority.class.isInstance(authority)) {
                    OAuth2UserAuthority oauth2UserAuthority = (OAuth2UserAuthority)authority;

                    Map<String, Object> userAttributes = oauth2UserAuthority.getAttributes();

                    // Map the attributes found in userAttributes
                    // to one or more GrantedAuthority's and add it to mappedAuthorities

                }
            });

            return mappedAuthorities;
        };
    }
}
```

또는 다음 예제와 같이 GrantedAuthoritiesMapper @Bean을 구성에 자동으로 적용하도록 등록 할 수 있습니다.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(withDefaults());
    }

    @Bean
    public GrantedAuthoritiesMapper userAuthoritiesMapper() {
        ...
    }
}
```

### Delegation-based strategy with OAuth2UserService
이 전략은 GrantedAuthoritiesMapper를 사용하는 것에 비해 고급이지만 OAuth2UserRequest 및 OAuth2User (OAuth 2.0 UserService를 사용하는 경우) 또는 OidcUserRequest 및 OidcUser (OpenID Connect 1.0 UserService를 사용할 경우)에 액세스 할 수있어 더욱 유연합니다.
OAuth2UserRequest (및 OidcUserRequest)는 관련 OAuth2AccessToken에 대한 액세스를 제공합니다. 이는 위임자가 보호 된 리소스에서 권한 정보를 가져와야 사용자에 대한 사용자 지정 권한을 매핑 할 수있는 경우에 매우 유용합니다.
다음 예는 OpenID Connect 1.0 UserService를 사용하여 위임 기반 전략을 구현하고 구성하는 방법을 보여줍니다.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .userInfoEndpoint(userInfoEndpoint ->
                        userInfoEndpoint
                            .oidcUserService(this.oidcUserService())
                            ...
                    )
            );
    }

    private OAuth2UserService<OidcUserRequest, OidcUser> oidcUserService() {
        final OidcUserService delegate = new OidcUserService();

        return (userRequest) -> {
            // Delegate to the default implementation for loading a user
            OidcUser oidcUser = delegate.loadUser(userRequest);

            OAuth2AccessToken accessToken = userRequest.getAccessToken();
            Set<GrantedAuthority> mappedAuthorities = new HashSet<>();

            // TODO
            // 1) Fetch the authority information from the protected resource using accessToken
            // 2) Map the authority information to one or more GrantedAuthority's and add it to mappedAuthorities

            // 3) Create a copy of oidcUser but use the mappedAuthorities instead
            oidcUser = new DefaultOidcUser(mappedAuthorities, oidcUser.getIdToken(), oidcUser.getUserInfo());

            return oidcUser;
        };
    }
}
```

### Configuring a Custom OAuth2User
CustomUserTypesOAuth2UserService는 사용자 정의 OAuth2User 유형을 지원하는 OAuth2UserService의 구현입니다.
기본 구현 (DefaultOAuth2User)이 사용자 요구에 맞지 않으면 고유 한 OAuth2User 구현을 정의 할 수 있습니다.
다음 코드는 GitHub에 대한 사용자 정의 OAuth2User 유형을 등록하는 방법을 보여줍니다.

```
@EnableWebSecurity
public class OAuth2LoginSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .oauth2Login(oauth2Login ->
                oauth2Login
                    .userInfoEndpoint(userInfoEndpoint ->
                        userInfoEndpoint
                            .customUserType(GitHubOAuth2User.class, "github")
                            ...
                    )
            );
    }
}
```

다음 코드는 GitHub에 대한 사용자 정의 OAuth2User 유형의 예를 보여줍니다.

```
public class GitHubOAuth2User implements OAuth2User {
    private List<GrantedAuthority> authorities =
        AuthorityUtils.createAuthorityList("ROLE_USER");
    private Map<String, Object> attributes;
    private String id;
    private String name;
    private String login;
    private String email;

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return this.authorities;
    }

    @Override
    public Map<String, Object> getAttributes() {
        if (this.attributes == null) {
            this.attributes = new HashMap<>();
            this.attributes.put("id", this.getId());
            this.attributes.put("name", this.getName());
            this.attributes.put("login", this.getLogin());
            this.attributes.put("email", this.getEmail());
        }
        return attributes;
    }

    public String getId() {
        return this.id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @Override
    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLogin() {
        return this.login;
    }

    public void setLogin(String login) {
        this.login = login;
    }

    public String getEmail() {
        return this.email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
```

> id, name, login 및 email은 GitHub의 UserInfo Response에 반환 된 속성입니다. UserInfo Endpoint에서 리턴 된 자세한 정보는 "인증 된 사용자 가져 오기"에 대한 API 문서를 참조하십시오.

### OAuth 2.0 UserService
DefaultOAuth2UserService는 표준 OAuth 2.0 제공자를 지원하는 OAuth2UserService의 구현입니다.

> OAuth2UserService는 권한 부여 흐름 동안 클라이언트에 부여된 액세스 토큰을 사용하여 UserInfo endpoint에서 최종 사용자 (자원 소유자)의 사용자 특성을 가져와 OAuth2User 형식으로 AuthenticatedPrincipal을 반환합니다.




















