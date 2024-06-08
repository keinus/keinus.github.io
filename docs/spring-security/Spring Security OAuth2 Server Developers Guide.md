# Introduction
OAuth 2.0 지원을위한 사용 설명서입니다. OAuth 1.0의 경우 모든 것이 다르므로 사용 설명서를 참조하십시오.
이 사용 설명서는 두 부분으로 나뉩니다. 첫 번째는 OAuth 2.0 provider 용이고, 두 번째는 OAuth 2.0 클라이언트 용입니다. 공급자와 클라이언트 모두에게 가장 좋은 샘플 코드 소스는 통합 테스트 및 샘플 앱입니다.

## OAuth 2.0 Provider
OAuth 2.0 공급자 메커니즘은 OAuth 2.0 보호 자원 노출을 담당합니다. 구성에는 보호 된 리소스에 독립적으로 또는 사용자를 대신하여 액세스 할 수있는 OAuth 2.0 클라이언트를 설정하는 것이 포함됩니다. 공급자는 보호 된 리소스에 액세스하는 데 사용되는 OAuth 2.0 토큰을 관리하고 확인하여 이를 수행합니다. 해당되는 경우 공급자는 클라이언트에게 보호 된 리소스 (예 : 확인 페이지)에 대한 액세스 권한을 부여 할 수 있는지 확인하는 인터페이스도 제공해야합니다.

## OAuth 2.0 Provider Implementation
OAuth 2.0의 공급자 역할은 실제로 Authorization Service와 Resource Service 사이에 분할되어 있으며, 이들은 동일한 애플리케이션에 상주하지만 Spring Security OAuth를 사용하여 두 애플리케이션간에 분할하고 여러 공유 서비스를 공유 할 수 있습니다. 인증 서비스. 토큰에 대한 요청은 Spring MVC 컨트롤러 엔드 포인트에 의해 처리되며 보호 된 자원에 대한 액세스는 표준 Spring Security 요청 필터에 의해 처리됩니다. OAuth 2.0 Authorization Server를 구현하려면 Spring Security 필터 체인에 다음 엔드 포인트가 필요합니다.

- AuthorizationEndpoint는 권한 부여 요청을 처리하는 데 사용됩니다. 기본 URL : / oauth / authorize
- TokenEndpoint는 액세스 토큰 요청을 처리하는 데 사용됩니다. 기본 URL : / oauth / token

OAuth 2.0 리소스 서버를 구현하려면 다음 필터가 필요합니다.

- OAuth2AuthenticationProcessingFilter는 인증 된 액세스 토큰이 제공된 요청에 대한 인증을 로드하는 데 사용됩니다.

## Authrization Server(권한서버) 설정
Authorization Server를 설정할 때는 grant type을 고민해야 합니다. grant type은 client가 end-user로부터 access token을 획득하기 위해 사용합니다 (예. authorization code, user credentials, refresh token을 획득할 필요가 있는 경우). 이 설정은 client details service와 token service를 구현하기 위해서 사용됩니다. 또한, 특정 권한 메커니즘과 access grants를 글로벌 영역에서 사용가능/불가능 상태로 만들기 위해 사용됩니다. 그러나 각 client는 특정 권한 메커니즘과 access grants를 사용하도록 설정될 수 있다는 점을 명심해야 합니다. 다시 말하자면, 단지 provider가 “client credentials” grant type을 지원하도록 설정되어있기 때문이지 특정 client가 그런 grant type으로 권한이 부여됨을 의미하지는 않습니다.

@EnableAuthorizationServer 어노테이션은 OAuth2.0 권한서버 메커니즘을 설정하기 위해 사용되며, AuthorizationServerConfigurer를 구현한 어떠한 @Beans와도 함께 사용됩니다 (비어있는 메서드로 되어있는 간편한 adapter 구현체가 있음). 아래 특징은 Spring에서 만든 분할된 설정들로 대표적인 요소이며, AuthorizationServerConfigurer의 일부입니다.

- ClientDetailsServiceConfigurer : client detail service를 정의하는 configurer. client 상세정보는 초기화될 수 있으며, 단순히 이미 존재하는 저장소를 참조하도록 할 수도 있습니다.
- AuthorizationServerSecurityConfigurer : token endpoint의 보안제약사항을 정의합니다.
- AuthorizationServerEndpointsConfigurer : 권한/token end point들을 정의하고 token service들도 정의합니다.

provide 설정의 중요한 점은 authorization code(권한코드)가 OAuth client에게 공급되는 방법입니다 (권한코드 grant에서). Authorization code는 OAuth client가 end-user를 권한페이지로 유도함으로써 획득됩니다. 권한페이지에서 user는 자격을 통과할 수 있고 결과적으로 provider authorization server에서 OAuth client로 authorization code를 재전송합니다. 이에 대한 예제들은 OAuth2 명세에 자세히 나와있습니다.

XML 에서는 <authorization-server/> 엘레먼트가 있어서 OAuth2.0 Authorization Server를 설정하는 방법과 비슷하게 사용됩니다.

### Configuring Client Details
ClientDetailsServiceConfigurer(AuthorizationServerConfigurer에서 콜백)은 in-memory나 JDBC로 구현된 client details service로 정의될 수 있습니다. client의 중요한 속성은 다음과 같습니다.

- clientId : (필수) client의 id
- secret : (신뢰되는 client에서 필수) client secret
- scope : client가 제한된 범위. scope가 정의되지 않았거나 비어있으면(기본설정) client는 scope에 제한을 받지 않습니다.
- authorizedGrantTypes : client가 사용하기 위해 권한을 획득한 grant type. 기본설정 값은 빈 값입니다.
- authorities : client가 받은 권한. (일반적인 spring security authorities)

client 상세정보는 애플리케이션 구동 중에도 저장소(예를 들면 JdbcClientDetailsService의 데이터베이스 테이블과 같은)나 ClientDetailsManager 인터페이스(ClientDetailsServicedml 구현체와 그 밖의 구현체)에 직접 접근하여 갱신될 수 있습니다.

주의 : JDBC service의 스키마는 라이브러리에 패키지화 되어있지 않습니다 (왜냐하면 작업 시 사용하길 원하는 방식이 너무나도 많을 수 있기 때문입니다). 하지만 github의 테스트코드에 예제가 있으니 처음 해볼 때에도 도움이 될 것이라 생각합니다.


### Managing Tokens
AuthorizationServerTokenServices 인터페이스는 OAuth 2.0 token을 관리하는 필수 동작을 정의합니다. 아래 내용을 명심하세요.

- access token이 만들어졌을 때, 그 인증정보는 반드시 저장되어야 합니다. 그래야 access token을 받는 resource들이 나중에 참조할 수 있습니다.
- access token은 생성 시 획득했던 권한을 담은 인증정보를 불러오기 위해 사용됩니다.

AuthorizationServerTokenServices를 구현할 때, DefaultTokenServices를 사용할 지 고려할 수도 있습니다. DefaultTokenServices는 access token의 format과 저장소를 변경하기 위해 플러그인 될 수 있어 다양하게 사용 가능합니다. 기본적으로 token들은 랜덤 값으로 만들어지며, TokenStore로 대표되는 영구적인 token들로 저장되는 경우를 제외한 모든 경우에 제어 가능합니다. 기본 저장방식은 in-memory 구현이나, 그 외의 방식도 이용가능 합니다. 여기 몇 가지 구현방식을 소개해드리겠습니다.

- 기본 방식인 InMemoryTokenStore는 단일 서버에 완전 좋습니다(낮은 traffic과 실패 시 백업서버로 hot swap하지 않는 경우를 말함). 대부분의 프로젝트는 개발단계에서 이렇게 시작하고 구동할 것입니다. 그래야 의존성 없이 서버를 시작하기 쉽기 때문입니다.

- JdbcTokenStore는 JDBC version과 동일하게 관계형 데이터베이스에 token 정보를 저장합니다. 서버 간에 데이터베이스를 공유한다면 이 방식을 사용하세요. 하나의 서버가 있다면 해당 서버의 크기를 키우고, 여러 컴포넌트가 존재한다면 Authorization Server와 Resources Server의 크기를 키우시면 됩니다. JdbcTokenStore를 사용하기 위해서는 “spring-jdbc”가 classpath에 있어야합니다.

- JSON Web Token(JWT) version의 저장방식에서는 token이 갖고 있는 모든 정보를 암호화합니다 (그래서 back end 어디에도 저장하지 않는다는 점이 주요 장점임). 한가지 단점은 access token을 쉽게 불러올 수 없다는 것입니다. 그래서 보통은 짧은 만료기간으로 발급되어 refresh token으로 제어됩니다. 또 다른 단점은 많은 user credential 정보를 저장하고 있다면, token들이 매우 커질 수 있다는 것입니다. JwtTokenStore는 데이터를 영구적으로 관리하는 진짜 “저장소”가 아니라, DefaultTokenServices 안에서 token값과 권한정보를 번역하는 역할을 합니다.

주의 : JDBC service의 스키마는 라이브러리에 패키지화 되어있지 않습니다 (왜냐하면 작업 시 사용하길 원하는 방식이 너무나도 많기 때문입니다). 하지만 github의 테스트코드에 예제가 있으니 처음 해보는데 도움이 될 것이라 생각합니다. token들이 동일한 row를 획득하려고 경쟁하는 경우 client 앱들 사이에 충돌을 예방하기 위해서 @EnableTransactionManagement를 반드시 사용해주세요. 한가지 더 주의할 점은 샘플 스키마는 분명한 PRIMARY KEY 정의를 갖습니다. – 이 부분은 공존환경에서도 역시 필수적입니다.

### JWT tokens
JWT 토큰을 사용하기 위해서는 Authorization Server에 JwtTokenStore이 필요합니다. Resource Server는 JWT 토큰을 복호화 할 수 있어야 합니다. 그래서 JwtTokenStore는 JwtAccessTokenConverter에 의존성을 갖게 되고, 동일한 구현체는 Authorization Server와 Resource Server 양쪽에 모두 필수입니다. token들은 기본적으로 서명되며, Resource Server 역시 서명을 확인할 수 있어야 합니다. 그러므로 Authorization Server로써 갖는 대칭키(서명 키 역할)가 필요하거나, Authorization Server안에 개인키(서명 키)와 매칭되는 공개키(확인 키)가 필요합니다 (공개-개인 또는 비대칭 키). 공개키는 Authorization Server의 /oauth/token_key endpoint에서 나타내며, 기본적으로 “denyAll()” 접근규칙으로 보호됩니다. AuthorizationServerSecurityConfigurer에 SpEL 표현을 주입하면 이를 확인해볼 수 있습니다. (예를 들어, “permitAll()”은 공개키이기 때문에 아마도 적합할 것입니다.)

JwtTokenStore를 사용하기 위해서는 classpath에 “spring-security-jwt”를 가지고 있어야 합니다 (Spring OAuth github 저장소에 같이 있으나, 배포주기는 다릅니다).


### Grant Types
grant type은 AuthorizationEndpoint에서 지원하며, AuthorizationServerEndpointsConfigurer를 통해 설정할 수 있습니다. 기본설정으로 모든 grant type들은 password를 제외하여 제공됩니다 (이를 사용하기 위해서 어떻게 해야 하는지 아래에서 확인). 아래의 속성으로 grant type을 바꿀 수 있습니다.

- authenticationManager : password 권한은 AuthenticationManager를 주입하여 사용합니다.
- userDetailsService : UserDetailsService를 주입하거나, 글로벌 영역에서 뭔가 하나가 설정되어있다면(예를 들면 GlobalAuthenticationManagerConfigurer 내에서) refresh token 권한은 user 상세정보를 검사하는 내용을 포함할 것입니다. 이는 해당 계정이 여전히 활성화되어 있는지 확인하기 위해서입니다.
- authorizationCodeService : auth code 부여를 위한 인증 코드 서비스(AuthorizationCodeService 인스턴스)를 정의합니다.
- implicitGrantService : 암묵적 권한에서 상태를 관리합니다.
- tokenGranter : TokenGranter (다른 상위 속성권한을 부여하거나 거부하는 모든 역할을 획득)

XML에서 권한 부여 유형은 authorization-server의 하위 요소로 포함됩니다.

### Configuring the Endpoint URLs
AuthorizationServerEndpointsConfigurer 는 pathMapping() 메서드를 갖고 있으며, 두 개의 인자값이 있습니다.

- endpoint를 위한 URL경로의 기본 값
- custom 경로 필수 값 (“/”로 시작함)

프레임워크에서 제공하는 URL경로는 

- /oauth/authorize (authorization endpoint)
- /oauth/token (token endpoint)
- /oauth/confirm_access (user는 권한획득을 위한 승인을 여기서 보냄)\
- /oauth/error (authorization server에서 에러를 보내기 위해 사용)
- /oauth/check_token (access token을 복호화하기 위해 Resource Server에서 사용됨)
- /oauth/token_key (JWT 토큰일 경우 공개키 보여줌)

중요 : Authorization endpoint /oauth/authorize (또는 변경된 경로, 경로변경 가능함)는 Spring Security를 사용하여 보호되어야 합니다. 그래야만 인증된 user들에게 접근 가능합니다. 예를 들면, 표준 Spring Security인 WebSecurityConfigurer를 사용합니다.

```
   @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests().antMatchers("/login").permitAll().and()
        // default protection for all resources (including /oauth/authorize)
            .authorizeRequests()
                .anyRequest().hasRole("USER")
        // ... more configuration, e.g. for form login
    }
```

주의 : 만약 Authorization Server가 Resource Server 이기도 하다면, API resources들을 관리하는 더 낮은 순위의 security filter chain도 하나 더 있습니다. access token으로 보호받는 이런 요청들을 위해서 주요 user-facing filter chain에서 특정한 것으로 매칭되지 않는 경로가 필요합니다. 그러므로 위의 WebSecurityConfigurer에서 오직 non-API resource만을 선택하는 request matcher가 포함되도록 해야 합니다.

Spring OAuth에서는 @Configuration으로 token endpoint는 기본적으로 보호받으며, client의 HTTP Basic authentication 사용을 지원합니다. XML의 경우는 아닙니다. (왜냐하면 명시적으로 보호되어야 하기 때문입니다)

XML에서는 <authorization-server/> 엘레먼트가 기본 endpoint URL을 변경하기 위한 속성을 비슷한 방식으로 제공합니다. /check_token endpoint는 명시적으로 사용 가능해야 합니다 (check-token-enabled 속성을 이용하시면 됩니다).


## Customizing the UI
대부분의 Authorization Server endpoint들은 주로 machine에 의해 동작하지만, 두 가지 resource는 UI가 필요합니다. 바로 GET요청이 되는 /oauth/confirm_access와 /oauth/error의 HTML 응답이 여기에 속합니다. 이 둘은 프레임워크 내에서 whitelabel 구현을 사용하여 제공됩니다. 그래서 Authorization Server의 실제 예의 대부분은 styling과 content를 제어할 수 있도록 하길 원할 것입니다. 여기서 해야 할 부분은 두 endpoint들을 위해서 @RequestMappings를 갖는 Spring MVC controller를 제공하는 것입니다. 그렇게 되면 프레임워크 기본설정은 dispatcher에서 낮은 우선순위를 얻게 될 것입니다. /oauth/confirm_access endpoint에서 AuthorizationRequest가 user의 승인을 받기 위해 필요한 모든 데이터를 소유한 세션으로 연결된다고 생각해도 좋습니다 (기본 구현은 WhitelabelApprovalEndpoint이니 복사하기 위해서는 그 곳의 시작지점을 살펴보시면 됩니다). 이렇게 요청된 모든 데이터를 가로채어 원하는 데로 변경하실 수 있습니다. 그러면, 모든 user들은 /oauth/authorize로 권한을 승인 또는 거부하는 내용을 포함한 POST응답을 하게 됩니다. 해당 요청 인자 값들은 AuthorizationEndpoint의 UserApprovalHandler로 직접 연결되어, 원하는 만큼 데이터를 더 많이 혹은 적게 해석할 수 있습니다. 기본 설정된 UserApprovalHanlder는 AuthorizationServerEndpointsConfigurer(이런 경우 ApprovalStoreUserApprovalHandler)이나 다른 경우에(이런 경우 TokenStoreUserApprovalHandler) ApprovalStore을 지원하는 지에 따라 달라집니다. 표준 approval handler들은 아래 내용을 따릅니다.

- TokenStoreUserApprovalHandler : user_oauth_approval가 “true” 혹은 “false” 여부에 따라 단순히 예/아니오로 결정.

- ApprovalStoreUserApprovalHandler : 요청된 scope와 일치하는 “*”를 갖는 scope.* 파라미터 키의 집합. 해당 파라미터의 값은 “true” 또는 “approved”가 될 수도 있고 아니면, user가 해당 scope에 거절당할 수도 있습니다. 권한은 최소한 하나의 scope가 승인된다면 성공입니다.

주의 : user에게 전달하는 form이 CSRF 보호를 포함해야 된다는 사실을 잊지 말아야 합니다. Spring Security는 기본 설정으로 요청 파라미터가 “_csrf”를 요청하길 예상합니다 (또한, 요청 속성 안에 포함된 값을 제공함). 더 자세한 내용을 위해서는 Spring Security user guide를 읽어보시거나, 가이드의 whitelabel 구현을 참고하시면 됩니다.

### Enforcing SSL
평문 HTTP는 테스트용으로는 좋지만, Authorization Server는 반드시 SSL을 통해 production 되어야 합니다. proxy와 container를 올바르게 설정했다면, secure container나 proxy 뒤에서 앱을 수행할 수 있습니다 (이 부분은 OAuth2에서 할 일이 없음). Spring Security requiresChannel() 제약을 사용하여 endpoint를 보호하려 할 수도 있습니다. /authorize는 endpoint를 일반적인 어플리케이션 보안의 한 부분으로 설정될 수 있습니다. /token endpoint는 AuthorizationServerEndpointsConfigurer에 flag가 있어서 sslOnly() 메소드를 사용할 지 설정할 수 있습니다. 두 경우에서 secure channel 설정은 선택적이지만, Spring Security가 insecure channel에서 요청을 발견한다면 설정된 곳으로 리다이렉트 하도록 만들어 줍니다.

## Customizing the Error Handling
Authorization Server의 error handling은 표준 Spring MVC의 특성을 이용합니다. 즉, endpoint에서 자신의 메서드를 @ExceptionHandler로 지칭합니다. user는 WebResponseExceptionTranslator를 자신의 endpoint에 제공하여 최선의 방법으로 응답 content를 변화시킬 수 있습니다. 반대의 경우 랜더링이 됩니다. token endpoint의 경우 exception의 랜더링을 HttpMessageConverters(이는 MVC설정으로 추가될 수 있습니다)에게 위임하고, authorization endpoint의 경우 OAuth error view(/oauth/error)에 위임합니다. whitelabel error endpoint는 HTML응답으로 제공되지만, user는 custom 구현을 원할 수 있습니다. (예를 들면, 단순히 @Controller를 @RequestMapping(“/oauth/error”)와 함께 추가할 수 있습니다).

## Mapping User Roles to Scopes
token의 scope 제한은 client에게 서명된 scope뿐만 아니라, user의 승인에 따라서 유용할 때가 있습니다. AuthorizationEndpoint에서 DefaultOAuth2RequestFactory를 사용하는 경우, flag를 checkUserScopes=true로 설정하여 user role에 매칭될 때만 승인되도록 제한을 줄 수 있습니다. OAuth2RequestFactory를 TokenEndpoint에 주입할 수도 있지만, 이 방법은 오직 TokenEndpointAuthenticationFilter를 설치한 경우에만 동작합니다 (예를 들면, password 권한일 경우). – HTTP BasicAuthenticationFilter 다음에 필터를 추가해야 합니다. 물론, 자기만의 규칙을 구현하여 mapping scope가 구현하신 버전의 OAuth2RequestFactory를 담당하고 설치하게 하실 수도 있습니다. AuthorizationServerEndpointsConfigurer는 custom OAuth2RequestFactoy를 주입하도록 허용하기 때문에 @EnableAuthorizationServer를 사용할 경우 이런 특징을 factory설정하기 위해 사용하실 수 있습니다.


## Resource Server Configuration
Resource Server(Authorization Server와 통합되거나 분리될 수도 있습니다)는 resource들이 OAuth2 token으로 보호받게 해줍니다. Spring OAuth는 이런 보호내용을 구현한 Spring Security 인증 필터를 제공합니다. @Configuration class에서 @EnableResourceServer로 전환할 수 있으며, ResourceServerConfigurer를 사용하여 설정할 수도 있습니다(필요하다면). 아래 특징은 설정 가능합니다.

- tokenServices : token service를 정의한 bean (ResourceServerTokenServices의 객체).
- resourceId : resource의 id (선택적이나, 권장되며 auth server에서 유효성 검증을 할 것입니다).
- resource server를 위한 다른 확장 지점 (예를 들어, 들어오는 요청으로부터 token을 추출하기 위해 tokenExtractor가 있습니다).
- Resource를 보호하기 위한 request matcher (모든 곳에서 기본 설정임).
- 보호받는 resource를 위한 접근 규칙 (기본으로 평문인 “authenticated”를 갖게 됨).
- Spring Security에서 HttpSecurity 설정에 의해 승인된 보호받는 resource를 위한 다른 customization.


@EnableResourceServer 어노테이션은 OAuth2AuthenticationProcessingFilter유형의 필터를 Spring Security filter chain에 자동으로 추가됩니다.
XML에서는 <resource-server/> 엘레먼트가 id 속성과 함께 제공됩니다. – id는 서블릿 Filter를 위한 bean id로 수동으로 표준 Spring Security chain에 추가될 수 있습니다.
ResourceServerTokenServices는 Authorization Server로 연결하기 위한 절반의 다른 부분입니다. Resource Server와 Authorization Server가 같은 어플리케이션에 속해 있고 DefaultTokenServices를 사용한다면, 이런 작업을 너무 어렵게 생각하실 필요는 없습니다. 왜냐하면, 이것이 모든 필요한 interface들을 구현하여 자동으로 일관되게 동작합니다. Resource Server가 분리된 어플리케이션이라면, Authorization Server능력을 일치시키고 token을 정확하게 복호화하는 방법을 알도록 ResourceServerTokenServices를 제공해야 합니다. Authorization Server에서 그랬듯이 DefaultTokenServices를 사용할 수 있으며, 대부분 TokenStore(backend storage나 local encoding)를 통해 표현됩니다. 대체 방법으로 RemoteTokenServices를 사용하여 Spring OAuth 특성을 사용하여 Resource Server가 Authorization Server(/oauth/check_token)의 HTTP resource를 통해 token을 복호화할 수도 있습니다. Resource Server에 엄청난 트래픽이 없거나(모든 요청은 Authorization Server에서 확인할 수 있어야 합니다), 결과를 캐싱할 수 있다면 RemoteTokenServices를 이용하는 방법이 편리합니다. /oauth/check_token endpoint를 사용하기 위해서는 AuthorizationServerSecurityConfigurer에서 access rule(기본은 “denyAll()”)을 변경시켜야 합니다. 아래는 해당 예제입니다.

```
		@Override
		public void configure(AuthorizationServerSecurityConfigurer oauthServer) throws Exception {
			oauthServer.tokenKeyAccess("isAnonymous() || hasAuthority('ROLE_TRUSTED_CLIENT')").checkTokenAccess(
					"hasAuthority('ROLE_TRUSTED_CLIENT')");
		}
```

이 예제에서 /oauth/check_token endpoint와 /oauth/token_key endpoint를 설정하고 있습니다(그러므로 신뢰하는 resource들은 JWT verification을 위한 공개키를 획득할 수 있습니다). 이 두 개의 endpoint는 client credentials를 사용하는 HTTP Basic authentication이 보호합니다.

### Configuring An OAuth-Aware Expression Handler
Spring Security의 expression-based accss control의 이점을 얻길 원할 수도 있습니다. expression handler는 기본적으로 @EnableResourceServer 설정으로 등록됩니다. expression은 #oauth2.clientHasRole과 #oauth2.clientHasAnyRole, #oauth2.denyClient를 포함하고 있으며, oauth client의 role에 따라 접근을 제공하기 위해 사용합니다(종합 목록을 위해서 OAuth2SecurityExpressionMethods을 확인하세요). XML에서는 <http/> 보안 설정의 expression-handler 엘레먼트를 이용하여 oauth-aware expression handler를 등록할 수 있습니다.


## OAuth 2.0 Client
OAuth 2.0 client 메커니즘은 다른 서버의 OAuth 2.0 보호 resource 접근을 책임집니다. 설정에서 관계된 보호 resource 구축내용을 포함하여 어떤 사용자가 접근가능한지를 설정합니다. client는 authorization code와 token을 저장하는 메커니즘을 user에게 제공해야 할 수도 있습니다.

### Protected Resource Configuration
보호 resource(혹은 “remote resource”)는 OAuth2ProtectedResourceDetails 유형의 bean 정의를 이용하여 정의될 수 있습니다. 보호 resource는 아래의 속성을 갖습니다.

- id : resource의 id. id는 오직 resource를 찾기 위해서 client가 사용합니다; 이런 내용은 OAuth 프로토콜에는 전혀 사용되지 않습니다. 또한, bean의 id로도 사용됩니다.
- clientId : OAuth client id. 어떤 OAuth provider가 client를 식별하는지를 확인하기 위한 id.
- clientSecret : resource와 연관된 secret. 기본으로 secret은 비어있지 않음.
- accessTokenUri : access token을 제공하는 provider OAuth endpoint의 URI.
- scope : resource로 접근하는 scope를 명시한 콤마분할 문자열 목록. 기본으로 scope는 설정되지 않음.
- clientAuthenticationScheme : client가 access token endpoint에 인증을 얻기 위해 사용하는 스키마. 제안 값 : “http_basic”과 “form”. 기본값 : “http_basic”. OAuth 2 스펙의 2.1항목을 확인하시면 됩니다.

다른 grant type은 OAuth2ProtectedResourceDetails의 다른 구체적인 구현을 갖습니다 (예를 들어 “client_credentials” grant type을 위해서는 ClientCredentialsResource을 사용). user authorization이 필요한 grant type을 위해서 더 많은 속성이 있습니다.

- userAuthorizationUri : user가 resource에 대해 access 권한을 영원히 얻어야 한다면, user가 리다이렉트될 uri. 이는 항상 필수는 아니고, 어떤 OAuth2 profile을 지원하는지에 달려있습니다.

XML에서는 <resource/> 엘레먼트가 있어서 OAuth2ProtectedResourceDetails 유형의 bean을 생성할 수 있습니다. 해당 엘레먼트는 위의 모든 속성을 연결할 속성을 갖고 있습니다.

### Client Configuration
OAuth 2.0 client는 @EnableOAuth2Client를 사용하여 단순하게 설정할 수 있습니다. 이는 2가지 역할을 수행합니다.

- filter bean을 만들어(oauth2ClientContextFilter ID로 만듦) 현재 요청과 context를 저장합니다. 인증이 필요한 경우, 요청되는 동안 OAuth authentication uri로 오가는 리다이렉션을 관리합니다.

- request scope내에 AccessTokenRequest 유형의 bean을 만듭니다. 이는 authorization code(or implicit) grant client에 의해 사용되어 충돌로부터 개인 user를 연관된 상태로 유지시킵니다.

해당 필터는 애플리케이션 내에 연결되어야 합니다 (예를 들어, 서블릿 initializer나 web.xml설정을 동일한 이름으로 DelegatingFilterProxy가 사용함).
AccessTokenRequest는 OAuth2RestTemplate에서 아래와 같이 사용될 수 있습니다.

```
@Autowired
private OAuth2ClientContext oauth2Context;

@Bean
public OAuth2RestTemplate sparklrRestTemplate() {
	return new OAuth2RestTemplate(sparklr(), oauth2Context);
}
```

OAuth2ClientContext는 session scope에 위치하여 다른 user들을 분리된 상태로 유지시킵니다. 서버에서 동등한 데이터 구조를 관리해야 할 필요 없이 user에게 요청되도록 매핑하고, 각 user가 분리된 OAuth2ClientContext 객체와 연결되도록 합니다.

XML에서는 <client/> 엘레먼트가 id 속성과 함께 제공됩니다 – 이는 서블릿 Filter의 bean id로, @Configuration에서 DelegatingFilterProxy로 매핑되는 경우와 같이 매핑되어야 합니다 (동일한 이름으로).

### Accessing Protected Resources
resource에 모든 설정을 지원한다면, 이제 해당 resource로 접근할 수 있습니다. 이런 resource에 접근하기 위해 제안된 메서드는 그 자체로 Spring3에서 소개된 해당 RestTemplate을 사용합니다. OAuth for Spring Security는 오직 OAuth2ProtectedResourceDetails 객체를 지원하기 위해 필요한 RestTemplate의 확장을 제공해왔습니다. user-token과 함께 이를 사용하기 위해서는(authorization code grants) @EnableOAuth2Client 설정을 사용할지 고민해볼 필요가 있습니다 (또는 XML로 <oauth:rest-template/>). 이런 설정은 context object로 범위가 설정된 몇몇 요청과 세션을 만들어서 실행 시에 서로 다른 user의 요청이 충돌하지 않도록 합니다.

일반적인 rule에서는 웹 애플리케이션이 password grants를 사용하지 말아야 합니다. 이는 AuthorizationCodeResourceDetails을 찬성할 수 있다면, ResourceOwnerPasswordResourceDetails의 사용을 피하기 위해서 입니다. 절실하게 password grants가 Java client에서 동작하려 하려 한다면, 동일한 메커니즘을 사용하여 OAuth2RestTemplate을 설정하고, ResourceOwnerPasswordResourceDetails(모든 access token사이에 공유됨)가 아닌 AccessTokenRequest(Map이고 수명이 짧음)에 대한 credential을 추가하시면 됩니다.

### Persisting Tokens in a Client
client는 token을 유지할 필요는 없지만, user가 client 앱이 재시작될 때마다 새로운 token grant를 승인할 필요는 없으므로 좋을 수 있습니다. ClientTokenServices interface는 OAuth 2.0 token이 특정 user에게 유지될 수 있도록 필수적인 동작을 정의합니다. JDBC구현이 제공되지만, access token과 영구적인 데이터베이스에 연관된 인증 객체를 저장하기 위해서 따로 서비스를 구현하길 원한다면 가능합니다. 이런 특징을 이용하길 원한다면, 특별히 설정된 TokenProvider에게 OAuth2RestTemplate을 제공해야 합니다. 아래는 예시입니다.

```
@Bean
@Scope(value = "session", proxyMode = ScopedProxyMode.INTERFACES)
public OAuth2RestOperations restTemplate() {
	OAuth2RestTemplate template = new OAuth2RestTemplate(resource(), new DefaultOAuth2ClientContext(accessTokenRequest));
	AccessTokenProviderChain provider = new AccessTokenProviderChain(Arrays.asList(new AuthorizationCodeAccessTokenProvider()));
	provider.setClientTokenServices(clientTokenServices());
	return template;
}
```

## Customizations for Clients of External OAuth2 Providers
외부 OAuth2 provider(예를 들어 Facebook)는 정확하게 상세내용을 구현하지 않습니다. 아니면, Spring Security OAuth보다 오래된 버전의 스펙에 따릅니다. Client 애플리케이션에서 그런 provider를 사용하기 위해서는 다양한 client-side infrastructure를 받아들여야 할 필요가 있습니다.

Facebook을 예제로 사용하기 위해서 torn2 애플리케이션에 Facebook 구현이 있습니다 (소유하신 서버와 유효성, client id와 secret을 설정에 추가하도록 변경해야 합니다 – Facebook 웹사이트에 만들기는 쉽습니다).

Facebook token 응답은 token의 만료시간을 표준을 지키지 않는 JSON entry에 포함되어 있습니다 (expires_in 대신 expires를 사용함). 그러므로 애플리케이션에서 만료시간을 사용하길 원한다면, OAuth2SerializationService를 수동으로 custom하여 복호화 되도록 해야만 합니다.
