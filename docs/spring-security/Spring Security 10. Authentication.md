---
layout: default
title: Spring Security 10. Authentication
nav_order: 1
parent: spring-security
---
                

# 10. Authentication
## 10.1 In-Memory Authentication
우리는 이미 단일 사용자에 대해 인 메모리 인증을 구성하는 예를 보았습니다. 다음은 여러 사용자를 구성하는 예입니다.

```
@Bean
public UserDetailsService userDetailsService() throws Exception {
    // ensure the passwords are encoded properly
    UserBuilder users = User.withDefaultPasswordEncoder();
    InMemoryUserDetailsManager manager = new InMemoryUserDetailsManager();
    manager.createUser(users.username("user").password("password").roles("USER").build());
    manager.createUser(users.username("admin").password("password").roles("USER","ADMIN").build());
    return manager;
}
```

## 10.2 JDBC Authentication
JDBC 기반 인증을 지원하기위한 업데이트를 찾을 수 있습니다. 아래 예제는 애플리케이션 내에 이미 DataSource를 정의한 것으로 가정합니다. jdbc-javaconfig 샘플은 JDBC 기반 인증을 사용하는 완전한 예를 제공합니다.

```
@Autowired
private DataSource dataSource;

@Autowired
public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
    // ensure the passwords are encoded properly
    UserBuilder users = User.withDefaultPasswordEncoder();
    auth
        .jdbcAuthentication()
            .dataSource(dataSource)
            .withDefaultSchema()
            .withUser(users.username("user").password("password").roles("USER"))
            .withUser(users.username("admin").password("password").roles("USER","ADMIN"));
}
```

## 10.8 AuthenticationProvider
### 10.8.1 AuthenticationProvider Java Configuration
사용자 정의 AuthenticationProvider를 Bean으로 노출하여 사용자 정의 인증을 정의
할 수 있습니다. 예를 들어, 다음은 SpringAuthenticationProvider가 AuthenticationProvider를 구현한다고 가정하여 인증을 사용자 정의합니다.

>AuthenticationManagerBuilder가 채워지지 않은 경우에만 사용됩니다

```
@Bean
public SpringAuthenticationProvider springAuthenticationProvider() {
    return new SpringAuthenticationProvider();
}
```


### 10.8.2 AuthenticationProvider XML Configuration
실제로 응용 프로그램 컨텍스트 파일에 추가 된 몇 가지 이름보다 확장 가능한 사용자 정보 소스가 필요합니다. 사용자 정보를 데이터베이스나 LDAP 서버와 같은 곳에 저장하려고 할 것입니다. LDAP 네임 스페이스 구성은 LDAP 장에서 다루므로 여기서 다루지 않습니다. 애플리케이션 컨텍스트에서 "myUserDetailsService"라는 Spring Security의 UserDetailsService를 사용자 정의 구현 한 경우 다음을 사용하여 이를 인증 할 수 있습니다.

```
<authentication-manager>
    <authentication-provider user-service-ref='myUserDetailsService'/>
</authentication-manager>
```

데이터베이스를 사용하려면 다음을 사용할 수 있습니다

```
<authentication-manager>
<authentication-provider>
    <jdbc-user-service data-source-ref="securityDataSource"/>
</authentication-provider>
</authentication-manager>
```

여기서 "securityDataSource"는 표준 Spring Security 사용자 데이터 테이블이 포함 된 데이터베이스를 가리키는 애플리케이션 컨텍스트의 DataSource Bean의 이름입니다. 또는 Spring Security JdbcDaoImpl Bean을 구성하고 user-service-ref 속성을 사용하여 지정할 수 있습니다.

```
<authentication-manager>
<authentication-provider user-service-ref='myUserDetailsService'/>
</authentication-manager>

<beans:bean id="myUserDetailsService"
    class="org.springframework.security.core.userdetails.jdbc.JdbcDaoImpl">
<beans:property name="dataSource" ref="dataSource"/>
</beans:bean>
```

다음과 같이 표준 AuthenticationProvider Bean을 사용할 수도 있습니다.

```
<authentication-manager>
    <authentication-provider ref='myAuthenticationProvider'/>
</authentication-manager>
```

여기서 myAuthenticationProvider는 응용 프로그램 컨텍스트에서 AuthenticationProvider를 구현하는 Bean의 이름입니다. 여러 인증 공급자 요소를 사용할 수 있으며,이 경우 공급자는 선언 된 순서대로 쿼리됩니다. 네임 스페이스를 사용하여 Spring Security AuthenticationManager를 구성하는 방법에 대한 자세한 내용은 10.11 절.“인증 관리자 및 네임 스페이스”를 참조하십시오.



## 10.9 UserDetailsService
사용자 정의 UserDetailsService를 Bean으로 노출하여 사용자 정의 인증을 정의 할 수 있습니다. 예를 들어, 다음은 SpringDataUserDetailsService가 UserDetailsService를 구현한다고 가정하여 인증을 사용자 정의합니다.

> AuthenticationManagerBuilder가 채워지지 않고 AuthenticationProviderBean이 정의되지 않은 경우에만 사용됩니다.

```
@Bean
public SpringDataUserDetailsService springDataUserDetailsService() {
    return new SpringDataUserDetailsService();
}
```

PasswordEncoder를 Bean으로 노출하여 비밀번호 인코딩 방법을 사용자 정의 할 수도 있습니다. 예를 들어, bcrypt를 사용하면 아래와 같이 Bean 정의를 추가 할 수 있습니다.

```
@Bean
public BCryptPasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();
}
```



## 10.10 Password Encoding
Spring Security의 PasswordEncoder 인터페이스는 비밀번호를 안전하게 저장하기 위해 비밀번호를 단방향으로 변환하는 데 사용됩니다. PasswordEncoder는 단방향 변환이므로 암호 변환이 양방향이어야하는 경우 (예 : 데이터베이스 인증에 사용되는 자격 증명 저장)는 아닙니다. 일반적으로 PasswordEncoder는 인증시 사용자가 제공 한 비밀번호와 비교해야하는 비밀번호를 저장하는 데 사용됩니다.


### 10.10.1 Password History
몇 년 동안 암호 저장을 위한 표준 메커니즘이 발전했습니다. 처음에는 암호가 일반 텍스트로 저장되었습니다. 비밀번호는 액세스하기 위해 credential 정보가 필수적으로 필요한 데이터 저장소에 저장되어 있으므로 비밀번호는 안전하다고 가정했습니다. 그러나 악의적 인 사용자는 SQL 인젝션과 같은 공격을 사용하여 사용자 이름과 암호의 큰 "데이터 덤프"를 얻는 방법을 찾을 수 있었습니다. 공공 보안 전문가는 점점 더 많은 사용자 자격 증명이 사용 됨에 따라 사용자 암호를 보호하기 위해 더 많은 작업을 수행하도록 요구했습니다. 
개발자는 SHA-256과 같은 단방향 해시를 통해 암호를 실행 한 후 저장하도록 권장되었습니다. 사용자가 인증을 시도하면 해시 된 비밀번호는 입력 한 비밀번호의 해시와 비교됩니다. 이것은 시스템이 암호의 단방향 해시를 저장하기만 하면됨을 의미했습니다. 위반이 발생하면 비밀번호의 단방향 해시만 노출됩니다. 해시를 만드는 방법은 한 가지 방법이었고 해시로 주어진 암호를 추측하는 것은 계산적으로 어려웠으므로 시스템의 각 암호를 알아내는 노력은 가치가 없습니다. 이 새로운 시스템을 없애기 위해 악의적인 사용자는 Rainbow Tables라고하는 조회 테이블을 만들기로 결정했습니다. 매번 각 암호를 추측하는 대신 암호를 한 번 계산하여 조회 테이블에 저장했습니다. Rainbow Tables의 효과를 완화하기 위해 개발자는 salt를 친 암호를 사용하도록 권장되었습니다. 해시 함수에 대한 입력으로 비밀번호만 사용하는 대신 모든 사용자의 비밀번호에 대해 임의 바이트 (소금)가 생성됩니다. 솔트와 사용자의 비밀번호는 고유 한 해시를 생성하는 해시 기능을 통해 실행됩니다. 소금은 사용자의 비밀번호와 함께 일반 텍스트로 저장됩니다. 그런 다음 사용자가 인증을 시도하면 해시 된 비밀번호는 저장된 솔트의 해시 및 입력 한 비밀번호와 비교됩니다. 고유 한 솔트는 해시가 모든 솔트 및 비밀번호 조합마다 다르기 때문에 Rainbow Tables가 더 이상 효과적이지 않음을 의미했습니다. 현대에는 SHA-256과 같은 암호화 해시가 더 이상 안전하지 않다는 것을 알고 있습니다. 최신 하드웨어를 사용하면 초당 수십억 개의 해시 계산을 수행 할 수 있기 때문입니다. 즉, 각 비밀번호를 쉽게 개별적으로 해독 할 수 있습니다. 개발자는 이제 적응 형 단방향 기능을 사용하여 비밀번호를 저장하는 것이 좋습니다. 적응 형 단방향 기능을 사용하여 암호를 검증하는 것은 의도적으로 리소스 (예 : CPU, 메모리 등)를 많이 사용합니다. 적응형 단방향 기능을 사용하면 하드웨어가 향상됨에 따라 "워크 팩터"를 구성 할 수 있습니다. "작업 요소"는 시스템의 암호를 확인하는 데 약 1 초가 걸리도록 조정하는 것이 좋습니다. 이 절충은 공격자가 암호를 해독하는 것을 어렵게 만들지만 비용이 많이 들지는 않지만 자체 시스템에 과도한 부담을줍니다. 스프링 시큐리티는 "작업 요소"에 대한 좋은 출발점을 제공하려고 시도했지만 성능은 시스템마다 크게 다르기 때문에 사용자는 자신의 시스템에 대해 "작업 요소"를 사용자 정의하는 것이 좋습니다. 사용해야하는 적응 형 단방향 함수의 예로는 bcrypt, PBKDF2, scrypt 및 Argon2가 있습니다. 적응 형 단방향 기능은 의도적으로 리소스를 많이 사용하므로 모든 요청에 ​​대해 사용자 이름과 비밀번호를 확인하면 응용 프로그램의 성능이 크게 저하됩니다. 유효성 검증 자원을 집중적으로 사용하여 보안을 확보하므로 스프링 보안 (또는 다른 라이브러리)이 비밀번호의 유효성 검증 속도를 높이기 위해 수행 할 수있는 것은 없습니다. 사용자는 장기 자격 증명 (예 : 사용자 이름 및 비밀번호)을 단기 자격 증명 (예 : 세션, OAuth 토큰 등)으로 교환하는 것이 좋습니다. 보안상의 손실없이 단기 자격 증명을 신속하게 검증 할 수 있습니다.


### 10.10.2 DelegatingPasswordEncoder
Spring Security 5.0 이전의 기본 PasswordEncoder는 일반 텍스트 비밀번호가 필요한 NoOpPasswordEncoder였습니다. 위의 Password History 섹션을 기반으로 기본 비밀번호 Encoder가 BCryptPasswordEncoder와 유사 할 것으로 예상 할 수 있습니다. 그러나 이것은 세 가지 실제 문제를 무시합니다.

- 이전 비밀번호 인코딩을 사용하여 쉽게 마이그레이션 할 수없는 많은 애플리케이션이 있습니다.
- 비밀번호 저장에 대한 모범 사례가 다시 변경될 수 있습니다.
- 프레임 워크로서 Spring Security는 자주 변경 사항을 적용할 수 없습니다.

대신 Spring Security는 DelegatingPasswordEncoder를 도입하여 다음과 같은 방법으로 모든 문제를 해결합니다.

- 현재 비밀번호 저장 권장 사항을 사용하여 비밀번호가 인코딩되도록 보장
- 최신 및 레거시 형식의 비밀번호 유효성 검사 허용
- 향후 인코딩 업그레이드 허용

PasswordEncoderFactories를 사용하여 DelegatingPasswordEncoder의 인스턴스를 쉽게 구성 할 수 있습니다.

```
PasswordEncoder passwordEncoder = PasswordEncoderFactories.createDelegatingPasswordEncoder();
```

또는 고유 한 사용자 지정 인스턴스를 만들 수도 있습니다. 예를 들면 다음과 같습니다.

```
String idForEncode = "bcrypt";
Map encoders = new HashMap<>();
encoders.put(idForEncode, new BCryptPasswordEncoder());
encoders.put("noop", NoOpPasswordEncoder.getInstance());
encoders.put("pbkdf2", new Pbkdf2PasswordEncoder());
encoders.put("scrypt", new SCryptPasswordEncoder());
encoders.put("sha256", new StandardPasswordEncoder());

PasswordEncoder passwordEncoder = new DelegatingPasswordEncoder(idForEncode, encoders);
```

### Password Storage Format
비밀번호의 일반적인 형식은 다음과 같습니다.

```
{id}encodedPassword
```

id는 사용해야하는 PasswordEncoder를 조회하는 데 사용되는 식별자이고 encodePassword는 PasswordEncoder를 사용하여 인코딩 된 비밀번호입니다. ID는 비밀번호의 시작 부분에 있어야하며 {로 시작하고}로 끝나야합니다. ID를 찾을 수 없으면 ID는 null입니다. 예를 들어, 다음은 다른 ID를 사용하여 인코딩 된 비밀번호 목록입니다. 원래 비밀번호는 모두 "password"입니다.

```
{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG 1
{noop}password 2
{pbkdf2}5d923b44a6d129f3ddf3e3c8d29412723dcbde72445e8ef6bf3b508fbf17fa4ed4d6b99ca763d8dc 3
{scrypt}$e0801$8bWJaSu2IKSn9Z9kM+TPXfOc/9bdYSrN1oD9qfVThWEwdRTnO7re7Ei+fUZRJ68k9lTyuTeUp4of4g24hHnazw==$OAOec05+bXxvuu/1qZ6NUR+xQYvYv7BeL1QxwRpY5Pc=  4
{sha256}97cde38028ad898ebc02e690819fa220e88c62e0699403e94fff291cfffaf8410849f27605abcbc0 5
```

1. Encoder ID : bcrypt, encodePassword : $2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG입니다. BCryptPasswordEncoder 사용.
2. Encoder ID : noop, encodePassword : password. NoOpPasswordEncoder 사용.
3. Encoder ID : pbkdf2, encodePassword : 5d923b44a6d129f3ddf3e3c8d29412723dcbde72445e8ef6bf3b508fbf17fa4ed4d6b99ca763d8dc. Pbkdf2PasswordEncoder 사용
4. Encoder ID : scrypt, encodePassword : $e0801$8bWJaSu2IKSn9Z9kM+TPXfOc/9bdYSrN1oD9qfVThWEwdRTnO7re7Ei+fUZRJ68k9lTyuTeUp4of4g24hHnazw==$OAOec05+bXxvuu/1qZ6NUR+xQYvYv7BeL1QxwRpY5Pc= SCryptPasswordEncoder 사용
5. Encoder ID : sha256, encodePassword : 97cde38028ad898ebc02e690819fa220e88c62e0699403e94fff291cfffaf8410849f27605abcbc0. StandardPasswordEncoder 사용.

> 일부 사용자는 잠재적 해커에게 저장소 형식이 제공되는 것을 우려 할 수 있습니다. 암호 저장소는 비밀인 알고리즘에 의존하지 않기 때문에 걱정할 필요가 없습니다. 또한 대부분의 형식은 공격자가 접두사없이 쉽게 파악할 수 있습니다. 예를 들어 BCrypt 암호는 종종 $2a$로 시작합니다.

### Password Encoding
생성자에 전달 된 idForEncode는 비밀번호 인코딩에 사용될 PasswordEncoder를 결정합니다. 위에서 생성 한 DelegatingPasswordEncoder에서, 이는 암호 인코딩 결과가 BCryptPasswordEncoder로 위임되고 {bcrypt}로 시작된다는 것을 의미합니다. 최종 결과는 다음과 같습니다.

```
{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

### Password Matching
{id}와 생성자에 제공된 PasswordEncoder에 대한 id의 맵핑을 기반으로 Matching이 수행됩니다. “Password Storage Format” 섹션의 예제는 이것이 수행되는 방법에 대한 실제 예를 제공합니다. 기본적으로 매핑되지 않은 ID(null ID 포함)와 암호를 사용하여 matches(CharSequence, String) 함수를 호출하면 IllegalArgumentException이 발생합니다. 이 동작은 DelegatingPasswordEncoder.setDefaultPasswordEncoderForMatches(PasswordEncoder)를 사용하여 사용자 정의 할 수 있습니다.
ID를 사용하면 모든 비밀번호 인코딩에서 일치 할 수 있지만 가장 최신 비밀번호 인코딩을 사용하여 비밀번호를 인코딩합니다. 암호화와 달리 암호 해시는 일반 텍스트를 복구하는 간단한 방법이 없도록 설계 되었기 때문에 중요합니다. 일반 텍스트를 복구 할 수있는 방법이 없으므로 암호를 마이그레이션하기가 어렵습니다. 사용자가 NoOpPasswordEncoder를 마이그레이션하는 것은 간단하기 때문에, 쉽게 프로젝트를 시작해볼 수 있도록 기본적으로 포함하도록 선택했습니다.

### Getting Started Experience
데모 또는 샘플을 작성하는 경우 사용자의 비밀번호를 해시하는 데 시간이 걸리는 것은 다소 번거로운 작업입니다. 이 작업을보다 쉽게 ​​수행 할 수있는 편리한 메커니즘이 있지만 여전히 프로덕션을 위한 것은 아닙니다.

```
User user = User.withDefaultPasswordEncoder()
  .username("user")
  .password("password")
  .roles("user")
  .build();
System.out.println(user.getPassword());
// {bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

여러 사용자를 작성하는 경우 빌더를 재사용 할 수도 있습니다.

```
UserBuilder users = User.withDefaultPasswordEncoder();
User user = users
  .username("user")
  .password("password")
  .roles("USER")
  .build();
User admin = users
  .username("admin")
  .password("password")
  .roles("USER","ADMIN")
  .build();
```

이렇게하면 저장된 비밀번호가 해시되지만 비밀번호는 여전히 메모리와 컴파일 된 소스 코드에 노출됩니다. 따라서 프로덕션 환경에서는 여전히 안전한 것으로 간주되지 않습니다. 프로덕션 환경에서는 비밀번호를 외부에서 해시해야합니다.

### Troubleshooting
저장된 비밀번호 중 하나에 "비밀번호 저장 형식"섹션에 설명 된대로 ID가없는 경우 다음 오류가 발생합니다.

```
java.lang.IllegalArgumentException: There is no PasswordEncoder mapped for the id "null"
    at org.springframework.security.crypto.password.DelegatingPasswordEncoder$UnmappedIdPasswordEncoder.matches(DelegatingPasswordEncoder.java:233)
    at org.springframework.security.crypto.password.DelegatingPasswordEncoder.matches(DelegatingPasswordEncoder.java:196)

```

오류를 해결하는 가장 쉬운 방법은 암호가 인코딩 된 PasswordEncoder를 명시 적으로 제공하도록 전환하는 것입니다. 이를 해결하는 가장 쉬운 방법은 현재 비밀번호가 저장되는 방법을 파악하고 올바른 PasswordEncoder를 명시 적으로 제공하는 것입니다. Spring Security 4.2.x에서 마이그레이션하는 경우 NoOpPasswordEncoder Bean을 노출하여 이전 동작으로 되돌릴 수 있습니다. 예를 들어, Java 구성을 사용하는 경우 다음과 같은 구성을 작성할 수 있습니다.

> NoOpPasswordEncoder로 되돌리는 것은 안전한 것으로 간주되지 않습니다. 보안 암호 인코딩을 지원하려면 DelegatingPasswordEncoder를 사용하여 마이그레이션해야합니다.

```
@Bean
public static NoOpPasswordEncoder passwordEncoder() {
    return NoOpPasswordEncoder.getInstance();
}
```

XML 구성을 사용하는 경우 id passwordEncoder를 사용하여 PasswordEncoder를 노출시킬 수 있습니다.

```
<b:bean id="passwordEncoder"
        class="org.springframework.security.crypto.password.NoOpPasswordEncoder" factory-method="getInstance"/>
```

또는 모든 비밀번호 앞에 올바른 ID를 붙여 DelegatingPasswordEncoder를 계속 사용할 수 있습니다. 예를 들어 BCrypt를 사용하는 경우 다음과 같은 비밀번호를 사용하여 비밀번호를 마이그레이션합니다.

```
$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
==>
{bcrypt}$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HZWzG3YB1tlRy.fqvM/BG
```

맵핑의 전체 목록은 PasswordEncoderFactories의 Javadoc을 참조하십시오.


### 10.10.3 BCryptPasswordEncoder
BCryptPasswordEncoder 구현은 널리 지원되는 bcrypt 알고리즘을 사용하여 비밀번호를 해시합니다. 암호 크래킹에 대한 저항력을 높이기 위해 bcrypt는 의도적으로 느립니다. 다른 적응 형 단방향 기능과 마찬가지로 시스템에서 암호를 확인하는 데 약 1 초가 걸리도록 조정해야합니다.

```
// Create an encoder with strength 16
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(16);
String result = encoder.encode("myPassword");
assertTrue(encoder.matches("myPassword", result));
```


### 10.10.4 Argon2PasswordEncoder
Argon2PasswordEncoder 구현은 Argon2 알고리즘을 사용하여 비밀번호를 해시합니다. Argon2는 Password Hashing Competition의 우승자입니다. 사용자 정의 하드웨어에서 암호 크래킹을 방지하기 위해 Argon2는 많은 양의 메모리가 필요한 고의로 느린 알고리즘입니다. 다른 적응 형 단방향 기능과 마찬가지로 시스템에서 암호를 확인하는 데 약 1 초가 걸리도록 조정해야합니다. Argon2PasswordEncoder에 BouncyCastle이 필요한 경우 현재 구현입니다.

```
// Create an encoder with all the defaults
Argon2PasswordEncoder encoder = new Argon2PasswordEncoder();
String result = encoder.encode("myPassword");
assertTrue(encoder.matches("myPassword", result));
```


### 10.10.5 Pbkdf2PasswordEncoder
Pbkdf2PasswordEncoder 구현은 PBKDF2 알고리즘을 사용하여 비밀번호를 해시합니다. 암호 크래킹을 없애기 위해 PBKDF2는 의도적으로 느린 알고리즘입니다. 다른 적응 형 단방향 기능과 마찬가지로 시스템에서 암호를 확인하는 데 약 1 초가 걸리도록 조정해야합니다. FIPS 인증이 필요한 경우이 알고리즘을 선택하는 것이 좋습니다.

```
// Create an encoder with all the defaults
Pbkdf2PasswordEncoder encoder = new Pbkdf2PasswordEncoder();
String result = encoder.encode("myPassword");
assertTrue(encoder.matches("myPassword", result));
```


### 10.10.6 SCryptPasswordEncoder
SCryptPasswordEncoder 구현은 암호화 알고리즘을 사용하여 비밀번호를 해시합니다. 사용자 지정 하드웨어 암호화에서 암호 크래킹을 방지하기 위해 많은 양의 메모리가 필요한 의도적으로 느린 알고리즘입니다. 다른 적응 형 단방향 기능과 마찬가지로 시스템에서 암호를 확인하는 데 약 1 초가 걸리도록 조정해야합니다.

```
// Create an encoder with all the defaults
SCryptPasswordEncoder encoder = new SCryptPasswordEncoder();
String result = encoder.encode("myPassword");
assertTrue(encoder.matches("myPassword", result));
```


### 10.10.7 Other PasswordEncoders
이전 버전과의 호환성을 위해 존재하는 상당수의 다른 PasswordEncoder 구현이 있습니다. 더 이상 안전한 것으로 간주되지 않기 때문에 더 이상 사용되지 않습니다. 그러나 기존 레거시 시스템을 마이그레이션하기 어렵 기 때문에 제거 할 계획이 없습니다.


### 10.10.8 Password Encoder XML Configuration
암호는 항상 목적에 맞게 설계된 보안 해싱 알고리즘을 사용하여 인코딩해야합니다 (SHA 또는 MD5와 같은 표준 알고리즘이 아님). 이것은 <password-encoder> 요소에 의해 지원됩니다. 암호화 된 암호를 암호화하면 원래 인증 공급자 구성은 다음과 같습니다.

```
<beans:bean name="bcryptEncoder"
    class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder"/>

<authentication-manager>
<authentication-provider>
    <password-encoder ref="bcryptEncoder"/>
    <user-service>
    <user name="jimi" password="$2a$10$ddEWZUl8aU0GdZPPpy7wbu82dvEw/pBpbRvDQRqA41y6mK1CoH00m"
            authorities="ROLE_USER, ROLE_ADMIN" />
    <user name="bob" password="$2a$10$/elFpMBnAYYig6KRR5bvOOYeZr1ie1hSogJryg9qDlhza4oCw1Qka"
            authorities="ROLE_USER" />
    </user-service>
</authentication-provider>
</authentication-manager>
```

다른 알고리즘을 사용해야하는 레거시 시스템이 없는 경우 bcrypt는 대부분의 경우에 적합한 선택입니다. 간단한 해싱 알고리즘을 사용하거나 일반 텍스트 암호를 저장하는 경우 bcrypt와 같은보다 안전한 옵션으로 마이그레이션하는 것을 고려해야합니다.



## 10.11 The Authentication Manager and the Namespace
Spring Security에서 인증 서비스를 제공하는 기본 인터페이스는 AuthenticationManager입니다. 이것은 일반적으로 Spring Security의 ProviderManager 클래스의 인스턴스이며, 이전에 프레임워크를 사용한 적이 있다면 이미 익숙 할 것입니다. 그렇지 않은 경우 technical overview 장에서 나중에 다룰 것입니다. Bean 인스턴스는 authentication-manager 네임스페이스 요소를 사용하여 등록됩니다. 네임스페이스를 통해 HTTP 또는 메소드 보안을 사용하는 경우 사용자 정의 AuthenticationManager를 사용할 수 없지만 사용되는 AuthenticationProvider를 완전히 제어 할 수 있으므로 문제가 되지 않습니다.
ProviderManager에 추가 AuthenticationProvider Bean을 등록하고 ref 속성과 함께 <authentication-provider> 요소를 사용하여 이를 수행 할 수 있습니다. 여기서 속성 값은 추가하려는 제공자 Bean의 이름입니다. 예를 들면 다음과 같습니다.

```
<authentication-manager>
<authentication-provider ref="casAuthenticationProvider"/>
</authentication-manager>

<bean id="casAuthenticationProvider"
    class="org.springframework.security.cas.authentication.CasAuthenticationProvider">
...
</bean>
```

또 다른 공통 요구 사항은 컨텍스트의 다른 Bean에 AuthenticationManager에 대한 참조가 필요할 수 있다는 것입니다. 당신은 쉽게 AuthenticationManager에 대한 별칭을 등록하고 응용 프로그램 컨텍스트에서 다른 곳이 이름을 사용할 수 있습니다.

```
<security:authentication-manager alias="authenticationManager">
...
</security:authentication-manager>

<bean id="customizedFormLoginFilter"
    class="com.somecompany.security.web.CustomFormLoginFilter">
<property name="authenticationManager" ref="authenticationManager"/>
...
</bean>
```



## 10.12 Session Management
HTTP 세션 관련 기능은 필터가 위임하는 SessionManagementFilter와 SessionAuthenticationStrategy 인터페이스의 조합으로 처리됩니다. 일반적인 사용에는 session-fixation 보호 공격 방지, 세션 시간 초과 감지 및 인증 된 사용자가 동시에 열 수있는 세션 수에 대한 제한이 포함됩니다.

### 10.12.1 Detecting Timeouts
유효하지 않은 세션 ID 제출을 감지하고 사용자를 적절한 URL로 리디렉션하도록 Spring Security를 ​​구성 할 수 있습니다. 이것은 session-management 요소를 통해 달성됩니다.

```
<http>
...
<session-management invalid-session-url="/invalidSession.htm" />
</http>
```

이 메커니즘을 사용하여 세션 시간 초과를 감지하면 사용자가 로그 아웃한 후 브라우저를 닫지 않고 다시 로그인하면 오류가 잘못보고 될 수 있습니다. 세션을 무효화 할 때 세션 쿠키가 지워지지 않고 사용자가 로그 아웃 한 경우에도 다시 제출되기 때문입니다. 로그 아웃 처리기에서 다음 구문을 사용하여 로그 아웃시 JSESSIONID 쿠키를 명시적으로 삭제할 수 있습니다.

```
<http>
<logout delete-cookies="JSESSIONID" />
</http>
```

불행히도 이것이 모든 서블릿 컨테이너에서 작동한다고 보장 할 수는 없으므로, 구축된 환경에서 테스트해봐야 합니다.

> 프록시 뒤에서 응용 프로그램을 실행중인 경우 프록시 서버를 구성하여 세션 쿠키를 제거 할 수도 있습니다. 예를 들어 Apache HTTPD의 mod_headers를 사용하는 다음 지시문은 로그 아웃 요청에 대한 응답으로 JSESSIONID 쿠키를 만료시켜 삭제합니다 (응용 프로그램이 /tutorial 경로에 배포되었다고 가정).
```
<LocationMatch "/tutorial/logout">
Header always set Set-Cookie "JSESSIONID=;Path=/tutorial;Expires=Thu, 01 Jan 1970 00:00:00 GMT"
</LocationMatch>
```


### 10.12.2 Concurrent Session Control
단일 사용자가 애플리케이션에 로그인 할 수 있는 기능을 제한하려는 경우 Spring Security는 다음과 같은 간단한 추가 기능을 통해 즉시 이를 지원합니다. 먼저 세션 수명주기 이벤트에 대해 Spring Security를 업데이트하려면 다음 리스너를 web.xml 파일에 추가해야합니다.

```
<listener>
<listener-class>
    org.springframework.security.web.session.HttpSessionEventPublisher
</listener-class>
</listener>
```

그런 다음 애플리케이션 컨텍스트에 다음 행을 추가하십시오.

```
<http>
...
<session-management>
    <concurrency-control max-sessions="1" />
</session-management>
</http>
```

이렇게하면 사용자가 여러 번 로그인 할 수 없습니다. 두 번째 로그인으로 첫 번째 로그인이 무효화됩니다. 종종 두 번째 로그인을 방지하고 싶을 때 사용할 수 있습니다.

```
<http>
...
<session-management>
    <concurrency-control max-sessions="1" error-if-maximum-exceeded="true" />
</session-management>
</http>
```

두 번째 로그인은 거부됩니다. "rejected"는 form 기반 로그인을 사용하는 경우 사용자가 인증 실패 URL로 전송됨을 의미합니다. "remember-me"와 같은 다른 비 대화식 메커니즘을 통해 두 번째 인증이 수행되면 "권한 없음"(401) 오류가 클라이언트로 전송됩니다. 대신 오류 페이지를 사용하려는 경우 session-authentication-error-url 속성을 session-management 요소에 추가 할 수 있습니다.

양식 기반 로그인에 사용자 정의 된 인증 필터를 사용하는 경우 동시 세션 제어 지원을 명시 적으로 구성해야합니다. 자세한 내용은 세션 관리 장에서 확인할 수 있습니다.


### 10.12.3 Session Fixation Attack Protection
Session Fixation 공격은 악의적 인 공격자가 사이트에 액세스하여 세션을 만든 다음 다른 사용자가 동일한 세션(예. 세션 식별자를 매개 변수로 포함하는 링크를 보내서)으로 로그인하도록 할 수있는 잠재적 위험입니다. Spring Security는 사용자가 로그인 할 때 새 세션을 생성하거나 세션 ID를 변경하여 자동으로 이를 방지합니다. 이 보호가 필요하지 않거나 다른 요구 사항과 충돌하는 경우 <session-management>의 session-fixation-protection 속성을 사용하여 동작을 제어 할 수 있습니다. 여기에는 4가지 옵션이 있습니다.

- none : 아무 것도하지 마십시오. 원래 세션이 유지됩니다.
- newSession : 기존 세션 데이터를 복사하지 않고 새 "깨끗한"세션을 만듭니다 (Spring Security 관련 특성은 계속 복사 됨).
- migrateSession : 새 세션을 작성하고 모든 기존 세션 속성을 새 세션으로 복사하십시오. 이것이 Servlet 3.0 또는 이전 컨테이너의 기본값입니다.
- changeSessionId : 새 세션을 만들지 마십시오. 대신, 서블릿 컨테이너(HttpServletRequest#changeSessionId())가 제공하는 session fixation 보호를 사용하십시오. 이 옵션은 Servlet 3.1 (JavaEE 7) 및 최신 컨테이너에서만 사용 가능합니다. 오래된 컨테이너에 지정하면 예외가 발생합니다. 이것이 Servlet 3.1 및 최신 컨테이너의 기본값입니다.

session fixation 보호가 발생하면 응용 프로그램 컨텍스트에 SessionFixationProtectionEvent가 발생됩니다. changeSessionId를 사용하는 경우 이 보호 기능으로 인해 javax.servlet.http.HttpSessionIdListener에 알림이 표시되므로 코드가 두 이벤트를 모두 수신하는 경우 주의하십시오. 추가 정보는 세션 관리 장을 참조하십시오.


### 10.12.4 SessionManagementFilter
SessionManagementFilter는 SecurityContextRepository의 내용을 SecurityContextHolder의 현재 내용과 비교하여 현재 요청 중에 사용자가 인증되었는지, 일반적으로 사전 인증 또는 remember-me와 같은 비 대화식 인증 메커니즘에 의해 인증되었는지 여부를 확인합니다 [4]. 리포지토리에 보안 컨텍스트가 포함 된 경우 필터는 아무 작업도 수행하지 않습니다. 그렇지 않은 경우 스레드 로컬 보안 컨텍스트에 익명이 아닌 인증 개체가 포함 된 경우 필터는 스택의 이전 필터에 의해 인증 된 것으로 가정합니다. 그런 다음 구성된 SessionAuthenticationStrategy를 호출합니다.
사용자가 현재 인증되지 않은 경우 필터는 유효하지 않은 세션 ID가 요청되었는지(예:시간 초과로 인해) 확인하고 구성된 InvalidSessionStrategy (설정된 경우)를 호출합니다. 가장 일반적인 동작은 고정 URL로 리디렉션하는 것이며 표준 구현 SimpleRedirectInvalidSessionStrategy에 캡슐화되어 있습니다. 후자는 또한 앞에서 설명한 것처럼 네임 스페이스를 통해 잘못된 세션 URL을 구성 할 때도 사용됩니다.

### 10.12.5 SessionAuthenticationStrategy
SessionAuthenticationStrategy는 SessionManagementFilter와 AbstractAuthenticationProcessingFilter에서 모두 사용되므로 사용자 정의 양식 로그인 클래스를 사용하는 경우 이를 두 가지 모두에 주입해야합니다. 이 경우 네임 스페이스와 사용자 정의 Bean을 결합한 일반적인 구성은 다음과 같습니다.

```
<http>
<custom-filter position="FORM_LOGIN_FILTER" ref="myAuthFilter" />
<session-management session-authentication-strategy-ref="sas"/>
</http>

<beans:bean id="myAuthFilter" class=
"org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter">
    <beans:property name="sessionAuthenticationStrategy" ref="sas" />
    ...
</beans:bean>

<beans:bean id="sas" class=
"org.springframework.security.web.authentication.session.SessionFixationProtectionStrategy" />
```

Spring 세션 범위 Bean을 포함하여 HttpSessionBindingListener를 구현하는 세션에 Bean을 저장하는 경우 기본 SessionFixationProtectionStrategy를 사용하면 문제가 발생할 수 있습니다. 자세한 정보는 이 클래스의 Javadoc을 참조하십시오.

### 10.12.6 Concurrency Control
Spring Security는 principal이 지정된 횟수 이상 동일한 응용 프로그램에 동시에 인증하는 것을 방지 할 수 있습니다. 많은 ISV는 이 기능을 사용하여 라이센스를 시행하는 반면, 네트워크 관리자는 사람들이 로그인 계정을 공유하지 못하도록 하기 때문에 이 기능을 좋아합니다. 예를 들어 "Batman"사용자가 두 개의 다른 세션에서 웹 응용 프로그램에 로그온하지 못하게 할 수 있습니다. 이전 로그인을 만료하거나 다시 로그인하려고 할 때 오류를 보고하여 두 번째 로그인을 막을 수 있습니다. 두 번째 방법을 사용하는 경우 명시적으로 로그 아웃하지 않은 (예 : 브라우저를 방금 닫은) 사용자는 원래 세션이 만료 될 때까지 다시 로그인 할 수 없습니다.
동시성 제어는 네임스페이스에서 지원되므로 가장 간단한 구성에 대해서는 이전 네임 스페이스 장을 확인하십시오. 때로는 구현을 커스터마이즈해야합니다.
구현시 ConcurrentSessionControlAuthenticationStrategy라는 특수화 된 버전의 SessionAuthenticationStrategy를 사용합니다.

> 이전에는 ConcurrentSessionController로 삽입 할 수있는 ProviderManager가 동시 인증을 확인했습니다. 후자는 사용자가 허용 된 세션 수를 초과하려고했는지 확인합니다. 그러나이 방법을 사용하려면 HTTP 세션을 미리 작성해야하므로 바람직하지 않습니다. Spring Security 3에서 사용자는 먼저 AuthenticationManager에 의해 인증되고 일단 성공적으로 인증되면 세션이 생성되고 다른 세션을 열 수 있는지 확인합니다.

동시 세션 지원을 사용하려면 web.xml에 다음을 추가해야합니다.

```
<listener>
    <listener-class>
    org.springframework.security.web.session.HttpSessionEventPublisher
    </listener-class>
</listener>
```

또한 ConcurrentSessionFilter를 FilterChainProxy에 추가해야합니다. ConcurrentSessionFilter에는 일반적으로 SessionRegistryImpl 인스턴스를 가리키는 sessionRegistry와 세션이 만료 될 때 적용 할 전략을 정의하는 sessionInformationExpiredStrategy라는 두 개의 생성자 인수가 필요합니다. 네임 스페이스를 사용하여 FilterChainProxy 및 기타 기본 Bean을 작성하는 구성은 다음과 같습니다.

```
<http>
<custom-filter position="CONCURRENT_SESSION_FILTER" ref="concurrencyFilter" />
<custom-filter position="FORM_LOGIN_FILTER" ref="myAuthFilter" />

<session-management session-authentication-strategy-ref="sas"/>
</http>

<beans:bean id="redirectSessionInformationExpiredStrategy"
class="org.springframework.security.web.session.SimpleRedirectSessionInformationExpiredStrategy">
<beans:constructor-arg name="invalidSessionUrl" value="/session-expired.htm" />
</beans:bean>

<beans:bean id="concurrencyFilter"
class="org.springframework.security.web.session.ConcurrentSessionFilter">
<beans:constructor-arg name="sessionRegistry" ref="sessionRegistry" />
<beans:constructor-arg name="sessionInformationExpiredStrategy" ref="redirectSessionInformationExpiredStrategy" />
</beans:bean>

<beans:bean id="myAuthFilter" class=
"org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter">
<beans:property name="sessionAuthenticationStrategy" ref="sas" />
<beans:property name="authenticationManager" ref="authenticationManager" />
</beans:bean>

<beans:bean id="sas" class="org.springframework.security.web.authentication.session.CompositeSessionAuthenticationStrategy">
<beans:constructor-arg>
    <beans:list>
    <beans:bean class="org.springframework.security.web.authentication.session.ConcurrentSessionControlAuthenticationStrategy">
        <beans:constructor-arg ref="sessionRegistry"/>
        <beans:property name="maximumSessions" value="1" />
        <beans:property name="exceptionIfMaximumExceeded" value="true" />
    </beans:bean>
    <beans:bean class="org.springframework.security.web.authentication.session.SessionFixationProtectionStrategy">
    </beans:bean>
    <beans:bean class="org.springframework.security.web.authentication.session.RegisterSessionAuthenticationStrategy">
        <beans:constructor-arg ref="sessionRegistry"/>
    </beans:bean>
    </beans:list>
</beans:constructor-arg>
</beans:bean>

<beans:bean id="sessionRegistry"
    class="org.springframework.security.core.session.SessionRegistryImpl" />
```

web.xml에 리스너를 추가하면 HttpSession이 시작되거나 종료 될 때마다 ApplicationEvent가 Spring ApplicationContext에 발생됩니다. 세션이 종료되면 SessionRegistryImpl에 알릴 수 있으므로 중요합니다. 이를 사용하지 않으면 사용자는 다른 세션에서 로그 아웃하거나 시간이 초과 되더라도 세션 허용 한도를 초과하면 다시 로그인 할 수 없습니다.

## 10.13 Remember-Me Authentication
### 10.13.1 Overview
Remember-me 또는 지속적 로그인 인증(로그인 유지)은 웹 사이트가 세션 간 principal의 ID를 기억할 수 있는 것을 말합니다. 이는 일반적으로 쿠키를 브라우저에 전송하여 향후 세션 중에 쿠키가 감지되고 자동 로그인이 발생하도록하여 수행됩니다. Spring Security는 이러한 작업을 수행하는 데 필요한 후크를 제공하며 두 가지 구체적인 Remember-me 구현이 있습니다. 하나는 해싱을 사용하여 쿠키 기반 토큰의 보안을 유지하고 다른 하나는 데이터베이스 또는 기타 영구 저장소 메커니즘을 사용하여 생성 된 토큰을 저장합니다.
두 구현 모두에는 UserDetailsService가 필요합니다. UserDetailsService를 사용하지 않는 인증 제공자(예:LDAP 제공자)를 사용하는 경우 애플리케이션 컨텍스트에 UserDetailsService Bean이 없으면 작동하지 않습니다.

### 10.13.2 Simple Hash-Based Token Approach
이 방법은 해싱을 사용하여 유용한 Remember-Me 전략을 달성합니다. 본질적으로 쿠키는 대화 형 인증에 성공하면 브라우저로 전송되며 쿠키는 다음과 같이 구성됩니다.
```
base64(username + ":" + expirationTime + ":" +
md5Hex(username + ":" + expirationTime + ":" password + ":" + key))

username:          ID. UserDetailsService에서 사용하는 식별자.
password:          password. UserDetailsService에서 ID와 함께 매칭하여 유저를 식별하는 값
expirationTime:    remember-me 토큰이 만료되는 날짜 및 시간 (밀리 초)
key:               remember-me 토큰의 수정을 방지하는 개인 키
```

그러므로 remember-me 토큰은 지정된 기간 동안만 유효하며 사용자 이름, 비밀번호 및 키가 변경되지 않는 경우에 한합니다. 특히, 이는 토큰이 만료 될 때까지 캡처 된 remember-me 토큰을 모든 사용자 에이전트에서 사용할 수 있다는 잠재적 보안 문제가 있습니다. 이것은 다이제스트 인증과 동일한 문제입니다. principal이 토큰이 캡처되었다는 것을 알고 있다면, 쉽게 암호를 변경하고 문제가있는 모든 remember-me 토큰을 즉시 무효화 할 수 있습니다. 보다 중요한 보안이 필요한 경우 다음 섹션에 설명 된 방법을 사용해야합니다. 또한 remember-me 서비스를 전혀 사용해서는 안됩니다.
네임스페이스 구성 장에서 논의 된 주제에 익숙한 경우 <remember-me> 요소를 추가하기 만하면 remember-me 인증을 사용할 수 있습니다.

```
<http>
...
<remember-me key="myAppKey"/>
</http>
```

UserDetailsService는 일반적으로 자동으로 선택됩니다. 애플리케이션 컨텍스트에 둘 이상이있는 경우 user-service-ref 속성과 함께 사용해야하는 것을 지정해야합니다. 여기서 값은 UserDetailsService Bean의 이름입니다.

### 10.13.3 Persistent Token Approach
이 접근법은 약간의 수정이있는 기사 http://jaspan.com/improved_persistent_login_cookie_best_practice[5]을 기반으로합니다. 네임스페이스 구성에 이 방법을 사용하려면 데이터 소스 참조를 제공해야합니다.

```
<http>
...
<remember-me data-source-ref="someDataSource"/>
</http>
```

데이터베이스에는 다음 SQL (또는 이와 동등한)을 사용하여 작성된 persist_logins 테이블이 포함되어야합니다.

```
create table persistent_logins (username varchar(64) not null,
                                series varchar(64) primary key,
                                token varchar(64) not null,
                                last_used timestamp not null)

```

### 10.13.4 Remember-Me Interfaces and Implementations
Remember-me는 UsernamePasswordAuthenticationFilter와 함께 사용되며 AbstractAuthenticationProcessingFilter 수퍼 클래스의 후크를 통해 구현됩니다. BasicAuthenticationFilter 내에서도 사용됩니다. 후크는 적절한 시간에 구체적인 RememberMeServices를 호출합니다. 인터페이스는 다음과 같습니다.

```
Authentication autoLogin(HttpServletRequest request, HttpServletResponse response);

void loginFail(HttpServletRequest request, HttpServletResponse response);

void loginSuccess(HttpServletRequest request, HttpServletResponse response,
    Authentication successfulAuthentication);
```

자세한 내용은 Javadoc을 참조하시고, 이 단계에서는 AbstractAuthenticationProcessingFilter는 loginFail() 및 loginSuccess() 메소드 만 호출한다는 점에 유의하여 보시면 되겠습니다. autoLogin() 메소드는 SecurityContextHolder가 Authentication을 가지고 있지 않으면 RememberMeAuthenticationFilter가 호출합니다. 따라서 이 인터페이스는 인증 관련 이벤트에 대한 충분한 알림과 함께 기본 remember-me 구현을 제공하며, 후보 웹 요청에 쿠키가 포함되어 있고 기억되고 싶을 때마다 구현에 위임합니다. 이 디자인은 많은 수의 remember-me 구현 전략을 허용합니다. 위에서 스프링 보안이 두 가지 구현을 제공한다는 것을 알았습니다. 이것들을 차례로 살펴 보겠습니다.

### TokenBasedRememberMeServices
이 구현은 10.13.2 절 “Simple Hash-Based Token Approach”에 설명 된 것 보다 간단한 접근 방식을 지원합니다. TokenBasedRememberMeServices는 RememberMeAuthenticationProvider에서 처리된 RememberMeAuthenticationToken을 생성합니다. key는 이 인증 공급자와 TokenBasedRememberMeServices간에 공유됩니다. 또한 TokenBasedRememberMeServices에는 서명 비교 목적으로 사용자 이름과 비밀번호를 검색하고 올바른 GrantedAuthority를 포함하는 RememberMeAuthenticationToken을 생성 할 수 있는 UserDetailsService가 필요합니다. 사용자가 요청하면 쿠키를 무효화하는 응용 프로그램에서 일종의 로그 아웃 명령을 제공해야합니다. TokenBasedRememberMeServices는 Spring Security의 LogoutHandler 인터페이스도 구현하므로 LogoutFilter와 함께 사용하여 쿠키를 자동으로 지울 수 있습니다.
remember-me 서비스를 사용하기 위해 애플리케이션 컨텍스트에 필요한 Bean은 다음과 같습니다.

```
<bean id="rememberMeFilter" class=
"org.springframework.security.web.authentication.rememberme.RememberMeAuthenticationFilter">
<property name="rememberMeServices" ref="rememberMeServices"/>
<property name="authenticationManager" ref="theAuthenticationManager" />
</bean>

<bean id="rememberMeServices" class=
"org.springframework.security.web.authentication.rememberme.TokenBasedRememberMeServices">
<property name="userDetailsService" ref="myUserDetailsService"/>
<property name="key" value="springRocks"/>
</bean>

<bean id="rememberMeAuthenticationProvider" class=
"org.springframework.security.authentication.RememberMeAuthenticationProvider">
<property name="key" value="springRocks"/>
</bean>
```

RememberMeServices 구현을 UsernamePasswordAuthenticationFilter.setRememberMeServices () 속성에 추가하고, AuthenticationManager.setProviders () 목록에 RememberMeAuthenticationProvider를 포함시키고, RememberMeAuthenticationFilter를 FilterChainProxy에 추가하십시오 (일반적으로 UsernamePasswordAuthenticationFilter 바로 다음에).

### PersistentTokenBasedRememberMeServices
이 클래스는 TokenBasedRememberMeServices와 같은 방식으로 사용될 수 있지만 토큰을 저장하려면 PersistentTokenRepository를 사용하여 추가로 구성해야합니다. 두 가지 표준 구현이 있습니다.

- InMemoryTokenRepositoryImpl : 테스트 전용
- JdbcTokenRepositoryImpl : 데이터베이스에 토큰을 저장

데이터베이스 스키마는 10.13.3 절. “Persistent Token Approach”에서 설명했습니다.

## 10.14 OpenID Support
네임 스페이스는 간단한 변경으로 일반 양식 기반 로그인 대신 또는 OpenID 로그인을 지원합니다.

```
<http>
<intercept-url pattern="/**" access="ROLE_USER" />
<openid-login />
</http>
```

그런 다음 OpenID 제공자 (예 : myopenid.com)에 등록하고 사용자 정보를 메모리 내 <user-service>에 추가해야합니다.

```
<user name="https://jimi.hendrix.myopenid.com/" authorities="ROLE_USER" />
```

myopenid.com 사이트를 사용하여 로그인하여 인증 할 수 있어야합니다. openid-login 요소에 user-service-ref 속성을 설정하여 OpenID를 사용하기 위해 특정 UserDetailsService Bean을 선택할 수도 있습니다. 자세한 내용은 인증 공급자에 대한 이전 섹션을 참조하십시오. 이 사용자 데이터 세트는 사용자의 권한을로드하는 데만 사용되므로 위의 사용자 구성에서 비밀번호 속성을 생략했습니다. 내부에서 임의의 암호가 생성되어 실수로이 사용자 데이터를 구성의 다른 곳에서 인증 소스로 사용할 수 없습니다.

### 10.14.1 Attribute Exchange
OpenID 속성 교환을 지원합니다. 예를 들어, 다음 구성은 애플리케이션에서 사용하기 위해 OpenID 제공자에서 이메일 및 전체 이름을 검색하려고 시도합니다.

```
<openid-login>
<attribute-exchange>
    <openid-attribute name="email" type="https://axschema.org/contact/email" required="true"/>
    <openid-attribute name="name" type="https://axschema.org/namePerson"/>
</attribute-exchange>
</openid-login>
```

각 OpenID 속성의 "유형"은 특정 스키마 (이 경우 https://axschema.org/)에 의해 결정된 URI입니다. 성공적인 인증을 위해 속성을 검색해야하는 경우 필요한 속성을 설정할 수 있습니다. 지원되는 정확한 스키마 및 속성은 OpenID 공급자에 따라 다릅니다. 속성 값은 인증 프로세스의 일부로 반환되며 다음 코드를 사용하여 나중에 액세스 할 수 있습니다.

```
OpenIDAuthenticationToken token =
    (OpenIDAuthenticationToken)SecurityContextHolder.getContext().getAuthentication();
List<OpenIDAttribute> attributes = token.getAttributes();
```

OpenIDAttribute는 속성 유형과 검색된 값 (또는 다중 값 속성의 경우 값)을 포함합니다. 기술 개요 장에서 핵심 Spring Security 구성 요소를 볼 때 SecurityContextHolder 클래스가 사용되는 방법에 대해 자세히 살펴 보겠습니다. 여러 ID 제공자를 사용하려는 경우 여러 속성 교환 구성도 지원됩니다. 각각의 식별자 일치 속성을 사용하여 여러 속성 교환 요소를 제공 할 수 있습니다. 여기에는 사용자가 제공 한 OpenID 식별자와 일치하는 정규식이 포함됩니다. Google, Yahoo 및 MyOpenID 제공자에 다른 속성 목록을 제공하는 구성 예제는 코드베이스의 OpenID 샘플 애플리케이션을 참조하십시오.

## 10.15 Anonymous Authentication
### 10.15.1 Overview
허용되는 대상을 명시적으로 지정하고 다른 모든 것을 허용하지 않는 "deny-by-default"를 채택하는 것이 일반적이고 관행적으로 좋은 보안 구성이라고 봅니다. 인증되지 않은 사용자가 액세스 할 수 있는 항목을 정의하는 것과 비슷한 상황(특히 웹 응용 프로그램의 경우)입니다. 많은 사이트에서는 사용자가 몇 개의 URL(예:홈 및 로그인 페이지) 이외 모든 다른 URL에 접근하려면 인증을 받아야합니다. 이 경우, 모든 URL에 보안을 설정하지 않고 특정 URL에만 액세스 구성 속성을 정의하는 것이 가장 쉽습니다. 달리 말해, 때로는 기본적으로 ROLE_SOMETHING이 필요하며 응용 프로그램의 로그인, 로그 아웃 및 홈 페이지와 같은 이 규칙에 대한 특정 예외 만 허용한다고 말하는 것이 좋습니다. 필터 체인에서 이러한 페이지를 완전히 생략하여 액세스 제어 검사를 생략 할 수 있지만, 다른 이유로 인해, 특히 인증 된 사용자 별로 별도 페이지 동작을 다르게 구성할 경우에는 바람직하지 않을 수 있습니다.
이것이 익명 인증의 의미입니다. "anonymously authenticated" 사용자와 인증되지 않은 사용자 사이에는 실질적인 개념적 차이가 없습니다. Spring Security의 익명 인증은 액세스 제어 속성을 보다 편리하게 구성 할 수있는 방법을 제공합니다. 예를 들어 getCallerPrincipal과 같은 서블릿 API 호출에 대한 호출은 실제로 SecurityContextHolder에 익명 인증 오브젝트가 있더라도 널을 리턴합니다.
감사 인터셉터가 SecurityContextHolder에 쿼리하여 주어진 작업을 담당 한 주체를 식별 할 때와 같이 익명 인증이 유용한 다른 상황이 있습니다. SecurityContextHolder에 항상 Authentication 객체가 포함되어 있고 null이 아닌 경우 클래스를 보다 강력하게 작성할 수 있습니다.

### 10.15.2 Configuration
익명 인증 지원은 HTTP 구성 Spring Security 3.0을 사용할 때 자동으로 제공되며 <anonymous> 요소를 사용하여 사용자 정의 (또는 비활성화) 할 수 있습니다. 기존 Bean 구성을 사용하지 않는 경우 여기에 설명 된 Bean을 구성 할 필요가 없습니다.
익명 인증 기능을 제공하는 세 가지 클래스가 있습니다. AnonymousAuthenticationToken은 Authentication의 구현이며 익명 사용자에 적용되는 GrantedAuthority를 저장합니다. AnonymousAuthenticationToken이 허용되도록 ProviderManager에 연결되는 AnonymousAuthenticationProvider가 있습니다. 마지막으로 AnonymousAuthenticationFilter가 있습니다. 이 필터는 일반 인증 메커니즘 이후 연결되며 기존에 Authentication이 없는 경우 AnonymousAuthenticationToken을 SecurityContextHolder에 자동으로 추가합니다. 필터 및 인증 공급자의 정의는 다음과 같이 나타납니다.

```
<bean id="anonymousAuthFilter"
    class="org.springframework.security.web.authentication.AnonymousAuthenticationFilter">
<property name="key" value="foobar"/>
<property name="userAttribute" value="anonymousUser,ROLE_ANONYMOUS"/>
</bean>

<bean id="anonymousAuthenticationProvider"
    class="org.springframework.security.authentication.AnonymousAuthenticationProvider">
<property name="key" value="foobar"/>
</bean>
```

key는 필터와 인증 공급자간에 공유되므로 전자가 만든 토큰이 후자에 의해 수락됩니다 [6]. userAttribute는 usernameInTheAuthenticationToken,grantedAuthority[, grantedAuthority]의 형식으로 표현됩니다. 이것은 InMemoryDaoImpl의 userMap 속성에서 등호 뒤에 사용 된 것과 동일한 구문입니다.

> [6] 키 속성의 사용이 여기서 실제 보안을 제공하는 것으로 간주되어서는 안됩니다. 그것은 단지 book-keeping 할 뿐 입니다. 인증 클라이언트가 인증 객체를 생성 할 수있는 시나리오(예 : RMI 호출)에서 AnonymousAuthenticationProvider가 포함된 ProviderManager를 공유하는 경우 악의적인 클라이언트는 자신이 만든 AnonymousAuthenticationToken을 제출할 수 있습니다(사용자 이름 및 권한 목록을 맘대로 선택하여). key가 추측 가능하거나 알 수 있는 경우 익명 제공자가 토큰을 승인합니다. 정상적인 사용에는 문제가되지 않지만 RMI를 사용하는 경우 HTTP 인증 메커니즘에 사용하는 공급자를 공유하는 대신 익명 공급자를 생략하는 사용자 정의 된 ProviderManager를 사용하는 것이 가장 좋습니다.

앞에서 설명한 것처럼 익명 인증의 이점은 모든 URI 패턴에 보안을 적용 할 수 있다는 것입니다. 예를 들면 다음과 같습니다.

```
<bean id="filterSecurityInterceptor"
    class="org.springframework.security.web.access.intercept.FilterSecurityInterceptor">
<property name="authenticationManager" ref="authenticationManager"/>
<property name="accessDecisionManager" ref="httpRequestAccessDecisionManager"/>
<property name="securityMetadata">
    <security:filter-security-metadata-source>
    <security:intercept-url pattern='/index.jsp' access='ROLE_ANONYMOUS,ROLE_USER'/>
    <security:intercept-url pattern='/hello.htm' access='ROLE_ANONYMOUS,ROLE_USER'/>
    <security:intercept-url pattern='/logoff.jsp' access='ROLE_ANONYMOUS,ROLE_USER'/>
    <security:intercept-url pattern='/login.jsp' access='ROLE_ANONYMOUS,ROLE_USER'/>
    <security:intercept-url pattern='/**' access='ROLE_USER'/>
    </security:filter-security-metadata-source>" +
</property>
</bean>
```



### 10.15.3 AuthenticationTrustResolver
익명 인증에 관한 내용 중 마지막은 AuthenticationTrustResolver 인터페이스 및 그 구현인 AuthenticationTrustResolverImpl입니다. 이 인터페이스는 isAnonymous(Authentication) 메소드를 제공하여 관심있는 클래스가 이 특수 유형의 인증 상태를 고려할 수 있도록합니다. ExceptionTranslationFilter는 이 인터페이스를 사용하여 AccessDeniedException을 처리합니다. AccessDeniedException이 발생하고 인증이 익명 유형인 경우 403(forbidden) 응답을 throw하는 대신 필터는 AuthenticationEntryPoint를 시작하여 principal이 올바르게 인증 할 수 있도록 할 것입니다. 이것은 필수적인 기능입니다. 그렇지 않으면 주체는 항상 "인증 된"것으로 간주되며 양식, 기본, 요약 또는 기타 일반 인증 메커니즘을 통해 로그인 할 수있는 기회가 주어지지 않습니다.
위의 인터셉터 구성에서 ROLE_ANONYMOUS 속성이 IS_AUTHENTICATED_ANONYMOUSLY로 대체 된 것을 종종 볼 수 있습니다. 이는 액세스 제어를 정의 할 때와 동일합니다. 이것은  authorization 장에서 볼 수있는 AuthenticatedVoter 사용의 예입니다. AuthenticationTrustResolver를 사용하여 이 특정 구성 속성을 처리하고 익명 사용자에게 액세스 권한을 부여합니다. AuthenticatedVoter 접근 방식은 익명의 사용자, Remember-Me 및 완전 인증 된 사용자를 구별 할 수 있게 하므로 더욱 강력합니다. 이 기능이 필요하지 않은 경우 ROLE_ANONYMOUS를 사용하면 Spring Security의 표준 RoleVoter에서 처리 할 수 있습니다.


## 10.16 Pre-Authentication Scenarios
권한 부여를 위해 Spring Security를 사용하고 싶지만 애플리케이션에 액세스하기 전에 다른 외부 시스템에서 사용자를 이미 인증하는 경우가 있습니다. 이러한 상황을 "pre-authenticated" 시나리오라고 합니다. 예를 들어 X.509, Siteminder 및 응용 프로그램이 실행중인 Java EE 컨테이너에 의한 인증이 있습니다. 사전 인증을 사용할 때 Spring Security는 다음과 같은 일을 합니다.

- 요청하는 사용자를 식별
- 사용자의 권한 확보

자세한 내용은 외부 인증 메커니즘에 따라 다릅니다. X.509의 경우 인증서 정보, 또는 Siteminder의 경우 HTTP 요청 헤더로 사용자를 식별 할 수 있습니다. 컨테이너 인증에 의존하는 경우 수신 HTTP 요청에서 getUserPrincipal() 메소드를 호출하여 사용자를 식별합니다. 어떤 경우에는 외부 메커니즘이 사용자에게 역할/권한 정보를 제공 할 수 있지만 다른 경우에는 권한이 UserDetailsService와 같은 별도의 소스에서 얻어야합니다.

이하 생략


## 10.17 Java Authentication and Authorization Service (JAAS) Provider
### 10.17.1 Overview
Spring Security는 인증 요청을 JAA (Java Authentication and Authorization Service)에 위임 할 수있는 패키지를 제공합니다. 이 패키지는 아래에서 자세히 설명합니다.

이하 생략

## 10.18 CAS Authentication
### 10.18.1 Overview
JA-SIG는 CAS로 알려진 전사적 싱글 사인온 시스템을 생성합니다. 다른 이니셔티브와 달리 JA-SIG의 중앙 인증 서비스는 오픈 소스이며 널리 사용되며 이해하기 쉽고 플랫폼에 독립적이며 프록시 기능을 지원합니다. Spring Security는 CAS를 완벽하게 지원하며 Spring Security의 단일 애플리케이션 배포에서 전사적 CAS 서버로 보호되는 다중 애플리케이션 배포에 이르기까지 쉬운 마이그레이션 경로를 제공합니다.

이하 생략

## 10.19 X.509 Authentication
### 10.19.1 Overview
X.509 인증서 인증의 가장 일반적인 용도는 SSL을 사용할 때 서버의 ID를 확인하는 것입니다. 가장 일반적으로 브라우저에서 HTTPS를 사용할 때입니다. 브라우저는 서버가 제공 한 인증서가 유지 관리하는 신뢰할 수있는 인증 기관 목록 중 하나에 의해 발급 (즉 디지털 서명)되었는지 자동으로 확인합니다.
"상호 인증"과 함께 SSL을 사용할 수도 있습니다. 그러면 서버는 SSL 핸드 셰이크의 일부로 클라이언트로부터 유효한 인증서를 요청합니다. 서버는 인증서가 수용 가능한 기관에 의해 서명되었는지 확인하여 클라이언트를 인증합니다. 유효한 인증서가 제공된 경우 애플리케이션의 서블릿 API를 통해 얻을 수 있습니다. Spring Security X.509 모듈은 필터를 사용하여 인증서를 추출합니다. 인증서를 애플리케이션 사용자에게 맵핑하고 표준 스프링 보안 인프라와 함께 사용하기 위해 해당 사용자의 권한 부여 기관을로드합니다.
Spring Security에서 인증서를 사용하기 전에 서블릿 컨테이너에 대한 인증서 사용 및 클라이언트 인증 설정에 익숙해야합니다. 대부분의 작업은 적합한 인증서와 키를 생성하고 설치하는 것입니다. 예를 들어 Tomcat을 사용하는 경우 https://tomcat.apache.org/tomcat-6.0-doc/ssl-howto.html의 지침을 읽으십시오. Spring Security로 시험해보기 전에 이 작업을 수행하는 것이 중요합니다.

이하 생략


## 10.20 Run-As Authentication Replacement
### 10.20.1 Overview
AbstractSecurityInterceptor는 보안 개체 콜백 단계에서 SecurityContext 및 SecurityContextHolder의 Authentication 개체를 임시로 바꿀 수 있습니다. 이는 원래 Authentication 객체가 AuthenticationManager 및 AccessDecisionManager에 의해 성공적으로 처리 된 경우에만 발생합니다. RunAsManager는 SecurityInterceptorCallback 동안 사용해야하는 대체 인증 오브젝트 (있는 경우)를 표시합니다.
보안 오브젝트 콜백 단계 중에 Authentication 오브젝트를 임시로 대체함으로써 보안 호출은 다른 인증 및 권한 정보가 필요한 또 다른 오브젝트를 호출 할 수 있습니다. 또한 특정 GrantedAuthority 오브젝트에 대한 내부 보안 점검을 수행 할 수 있습니다. Spring Security는 SecurityContextHolder의 내용을 기반으로 원격 프로토콜을 자동으로 구성하는 다수의 헬퍼 클래스를 제공하므로 이러한 run-as 대체는 원격 웹 서비스를 호출 할 때 특히 유용합니다.

### 10.20.2 Configuration
RunAsManager 인터페이스는 Spring Security에서 다음과 같이 제공됩니다.

```
Authentication buildRunAs(Authentication authentication, Object object,
    List<ConfigAttribute> config);

boolean supports(ConfigAttribute attribute);

boolean supports(Class clazz);
```

첫 번째 메소드는 메소드 호출 기간 동안 기존 Authentication 오브젝트를 대체해야하는 또 다른 Authentication 오브젝트를 리턴합니다. 메소드가 NULL을 리턴하면 교체를 수행하지 않아야 함을 나타냅니다. 두 번째 메소드는 구성 속성의 시작 유효성 검사의 일부로 AbstractSecurityInterceptor에서 사용됩니다. supports(Class) 메소드는 보안 인터셉터 구현에 의해 호출되어 구성된 RunAsManager가 보안 인터셉터가 제공 할 보안 오브젝트 유형을 지원하는지 확인합니다.
RunAsManager의 구체적인 구현은 Spring Security와 함께 제공됩니다. ConfigAttribute 중 RUN_AS_로 시작하는게 있으면 RunAsManagerImpl 클래스는 대체 RunAsUserToken을 반환합니다. 이러한 ConfigAttribute가 있으면 대체 RunAsUserToken에 각 RUN_AS_ConfigAttribute에 대한 새 SimpleGrantedAuthority와 함께 원래 인증 오브젝트와 동일한 principal, credentials, 권한이 포함됩니다. 각각의 새로운 SimpleGrantedAuthority는 ROLE_ 접두어 뒤에 RUN_AS ConfigAttribute가 붙습니다. 예를 들어, RUN_AS_SERVER는 ROLE_RUN_AS_SERVER 권한을 부여받은 대체 RunAsUserToken을 생성합니다.
대체 RunAsUserToken은 다른 Authentication 객체와 같습니다. 적절한 AuthenticationProvider에 위임을 통해 AuthenticationManager에 의해 인증되어야합니다. RunAsImplAuthenticationProvider는 이러한 인증을 수행합니다. 제시된 RunAsUserToken을 유효한 것으로 받아들입니다.
악의적인 코드가 RunAsUserToken을 생성하지 않고 RunAsImplAuthenticationProvider가 이를 수락하도록 제시하도록 하기 위해 키의 해시는 생성 된 모든 토큰에 저장됩니다. RunAsManagerImpl 및 RunAsImplAuthenticationProvider는 Bean 컨텍스트에서 동일한 키를 사용하여 작성됩니다.

```
<bean id="runAsManager"
    class="org.springframework.security.access.intercept.RunAsManagerImpl">
<property name="key" value="my_run_as_password"/>
</bean>

<bean id="runAsAuthenticationProvider"
    class="org.springframework.security.access.intercept.RunAsImplAuthenticationProvider">
<property name="key" value="my_run_as_password"/>
</bean>
```

동일한 키를 사용하여 승인 된 RunAsManagerImpl에 의해 작성된 각 RunAsUserToken의 유효성을 검증 할 수 있습니다. 보안상의 이유로 RunAsUserToken은 생성 후 변경할 수 없습니다.


## 10.21 Form Login
### 10.21.1 Form Login Java Configuration
HTML 파일이나 JSP에 대한 언급이 없기 때문에 로그인하라는 메시지가 표시 될 때 로그인 양식의 위치가 궁금 할 수 있습니다. Spring Security의 기본 구성은 로그인 페이지의 URL을 명시적으로 설정하지 않기 때문에, Spring Security는 활성화 된 기능을 기반으로 기본 값들을 사용하여 제출 된 로그인을 처리하는 URL 페이지를 자동으로 생성하며, 로그인 후 사용자에게 전송되는 기본 URL도 생성합니다.
자동으로 생성 된 로그인 페이지는 빠르게 시작하고 실행하는 것이 편리하지만 대부분의 응용 프로그램은 자체 로그인 페이지를 제공하려고합니다. 기본 구성을 변경하려면 앞에서 설명한 WebSecurityConfigurerAdapter를 다음과 같이 확장하여 사용자 정의 할 수 있습니다.

```
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
    // ...
}
```

그런 다음 아래와 같이 구성 방법을 재정의하십시오.

```
protected void configure(HttpSecurity http) throws Exception {
    http
        .authorizeRequests(authorizeRequests ->
            authorizeRequests
                .anyRequest().authenticated()
        )
        .formLogin(formLogin ->
            formLogin
                .loginPage("/login") 1
                .permitAll()         2
        );
}
```

1. 업데이트 된 구성은 로그인 페이지의 위치를 지정합니다. 
2. 모든 사용자 (즉, 인증되지 않은 사용자)에게 로그인 페이지에 대한 액세스 권한을 부여해야합니다. formLogin().permitAll() 메소드를 사용하면 양식 기반 로그인과 연관된 모든 URL에 대해 모든 사용자에게 액세스 권한을 부여 할 수 있습니다.

현재 구성을 위해 JSP로 구현 된 로그인 페이지 예는 다음과 같습니다.

> 아래의 로그인 페이지는 현재 구성을 나타냅니다. 일부 기본값이 요구 사항을 충족하지 않으면 구성을 쉽게 업데이트 할 수 있습니다.

```
<c:url value="/login" var="loginUrl"/>
<form action="${loginUrl}" method="post">       1
    <c:if test="${param.error != null}">        2
        <p>
            Invalid username and password.
        </p>
    </c:if>
    <c:if test="${param.logout != null}">       3
        <p>
            You have been logged out.
        </p>
    </c:if>
    <p>
        <label for="username">Username</label>
        <input type="text" id="username" name="username"/>  4
    </p>
    <p>
        <label for="password">Password</label>
        <input type="password" id="password" name="password"/>  5
    </p>
    <input type="hidden"                        6
        name="${_csrf.parameterName}"
        value="${_csrf.token}"/>
    <button type="submit" class="btn">Log in</button>
</form>
```

1. /login URL에 POST를 보내 사용자 인증을 시도합니다. 
2. 쿼리 매개 변수에 error가 있으면 인증을 시도하고 실패했습니다. 
3. 쿼리 매개 변수에 logout이 있으면 사용자가 성공적으로 로그 아웃되었습니다. 
4. username은 username이라는 HTTP 매개 변수로 존재해야합니다. 
5. password는 password라는 HTTP 매개 변수로 존재해야합니다. 
6. "CSRF 토큰 포함"섹션을 참조해야합니다. 자세한 내용은 5.1.1 절. "CSRF (Cross Site Request Forgery)"섹션을 참조하십시오.

### 10.21.2 Form Login XML Configuration
### Form and Basic Login Options
생략

## 10.22 Basic and Digest Authentication
기본 및 다이제스트 인증은 웹 응용 프로그램에서 널리 사용되는 대체 인증 메커니즘입니다. 기본 인증은 종종 각 요청마다 자격 증명을 전달하는 stateless 클라이언트와 함께 사용됩니다. 브라우저 기반 사용자 인터페이스와 웹 서비스를 통해 응용 프로그램을 사용하는 경우 form 기반 인증과 함께 사용하는 것이 일반적입니다. 그러나 기본 인증은 비밀번호를 일반 텍스트로 전송하므로 HTTPS와 같은 암호화 된 전송 계층을 통해서만 사용해야합니다.

### 10.22.1 BasicAuthenticationFilter
BasicAuthenticationFilter는 HTTP 헤더에 표시되는 기본 인증 자격 증명을 처리합니다. 이는 스프링 원격 프로토콜 (예 : Hessian 및 Burlap)과 일반 브라우저 사용자 에이전트(예: Firefox 및 Internet Explorer)에서 호출을 인증하는 데 사용할 수 있습니다. HTTP 기본 인증을 관리하는 표준은 RFC 1945, 섹션 11에 의해 정의되며 BasicAuthenticationFilter는 이 RFC를 준수합니다. 기본 인증은 사용자 에이전트에 광범위하게 배포되고 구현이 매우 간단하기 때문에 인증에 대한 매력적인 접근 방식입니다 (HTTP 헤더에 지정된 username : password의 Base64 인코딩 일뿐입니다).

### 10.22.2 Configuration
HTTP 기본 인증을 구현하려면 필터 체인에 BasicAuthenticationFilter를 추가해야합니다. 응용 프로그램 컨텍스트에는 BasicAuthenticationFilter와 필수 공동 작업자가 포함되어야합니다.

```
<bean id="basicAuthenticationFilter"
class="org.springframework.security.web.authentication.www.BasicAuthenticationFilter">
<property name="authenticationManager" ref="authenticationManager"/>
<property name="authenticationEntryPoint" ref="authenticationEntryPoint"/>
</bean>

<bean id="authenticationEntryPoint"
class="org.springframework.security.web.authentication.www.BasicAuthenticationEntryPoint">
<property name="realmName" value="Name Of Your Realm"/>
</bean>
```

구성된 AuthenticationManager는 각 인증 요청을 처리합니다. 인증이 실패하면 구성된 AuthenticationEntryPoint를 사용하여 인증 프로세스를 재 시도합니다. 일반적으로 필터를 BasicAuthenticationEntryPoint와 함께 사용하여 HTTP 기본 인증을 재 시도하기 위해 적절한 헤더와 함께 401 응답을 반환합니다. 인증에 성공하면 평소와 같이 결과 인증 오브젝트가 SecurityContextHolder에 배치됩니다.

인증 이벤트가 성공했거나 HTTP 헤더에 지원되는 인증 요청이 포함되어 있지 않아 인증을 시도하지 않은 경우 필터 체인은 정상적으로 계속 진행됩니다. 필터 체인이 중단되는 유일한 시간은 인증이 실패하고 AuthenticationEntryPoint가 호출 된 경우입니다.

## 10.23 DigestAuthenticationFilter
DigestAuthenticationFilter는 HTTP 헤더에 표시된 다이제스트 인증 자격 증명을 처리 할 수 ​​있습니다. 다이제스트 인증은 기본 인증의 많은 약점을 해결하려고 시도합니다. 특히 자격 증명이 일반 텍스트로 전송되지 않도록합니다. Mozilla Firefox 및 Internet Explorer를 포함한 많은 사용자 에이전트가 다이제스트 인증을 지원합니다. HTTP 다이제스트 인증을 관리하는 표준은 RFC 2617에 의해 정의되어 RFC 2069에 의해 규정 된 이전 버전의 다이제스트 인증 표준을 업데이트합니다. 대부분의 사용자 에이전트는 RFC 2617을 구현합니다. Spring Security의 DigestAuthenticationFilter는 "auth" 보호 품질 (qop)과 호환됩니다. RFC 2617에서 규정 한 RFC 2069와 역 호환성을 제공합니다. 다이제스트 인증은 암호화되지 않은 HTTP를 사용해야하는 경우(예: TLS / HTTPS 없음) 인증 프로세스의 보안을 최대화하려는 경우 더 매력적인 옵션입니다. 실제로 다이제스트 인증은 RFC 2518 섹션 17.1에 명시된 WebDAV 프로토콜의 필수 요구 사항입니다.

> Digest는 안전한 것으로 간주되지 않으므로 최신 응용 프로그램에서는 사용하지 않아야합니다. 가장 명백한 문제는 암호를 일반 텍스트, 암호화 또는 MD5 형식으로 저장해야한다는 것입니다. 이러한 모든 스토리지 형식은 안전하지 않은 것으로 간주됩니다. 대신 단방향 적응 형 암호 해시 (예 : bCrypt, PBKDF2, SCrypt 등)를 사용해야합니다.

중앙에서 다이제스트 인증은 "nonce"입니다. 이 값은 서버가 생성하는 값입니다. Spring Security의 nonce는 다음 형식을 채택합니다.

```
base64(expirationTime + ":" + md5Hex(expirationTime + ":" + key))
expirationTime:   nonce가 만료되는 날짜 및 시간 (밀리 초)
key:              nonce 토큰의 수정을 방지하기위한 개인 키
```

DigestAuthenticationEntryPoint에는 만료 시간을 결정하기 위한 nonceValiditySeconds 속성과 함께 nonce 토큰을 생성하는 데 사용되는 키를 지정하는 속성이 있습니다 (기본값 300, 5 분). nonce가 유효한 동안 다이제스트는 사용자 이름, 암호, nonce, 요청되는 URI, 클라이언트 생성 nonce (사용자 에이전트가 각 요청을 생성하는 임의의 값), 영역 이름 등을 포함한 다양한 문자열을 연결하여 계산됩니다. 그리고 MD5 해시를 수행합니다. 서버와 사용자 에이전트 모두 이 다이제스트 계산을 수행하여 포함 된 값 (예 : 비밀번호)에 동의하지 않으면 다른 해시 코드를 생성합니다. Spring Security 구현에서 서버에서 생성 된 nonce가 단지 만료 되었으나 (다이제스트가 유효하지 않은 경우) DigestAuthenticationEntryPoint는 "stale = true"헤더를 보냅니다. 이를 통해 사용자 에이전트는 사용자를 방해 할 필요가 없으며 (암호 및 사용자 이름 등이 정확하므로) 새로운 nonce를 사용하여 다시 시도하면됩니다. 
DigestAuthenticationEntryPoint의 nonceValiditySeconds 매개 변수에 적절한 값은 응용 프로그램에 따라 다릅니다. 매우 안전한 응용 프로그램은 가로 채기 된 인증 헤더를 사용하여 nonce에 포함 된 expirationTime에 도달 할 때까지 보안 주체를 가장 할 수 있습니다. 이것이 적절한 설정을 선택할 때의 주요 원칙이지만, 매우 안전한 응용 프로그램이 첫 번째 인스턴스에서 TLS / HTTPS를 통해 실행되지 않는 경우는 드문일 입니다. 
보다 복잡한 다이제스트 인증 구현으로 인해 종종 사용자 에이전트 문제가 있습니다. 예를 들어 Internet Explorer는 동일한 세션에서 후속 요청에 대해 "opaque"토큰을 제시하지 못합니다. 따라서 Spring Security 필터는 모든 상태 정보를 대신 "nonce"토큰으로 캡슐화합니다. 테스트에서 Spring Security의 구현은 Mozilla Firefox 및 Internet Explorer와 안정적으로 작동하여 nonce 시간 초과 등을 올바르게 처리합니다.

### 10.23.1 Configuration
이론을 검토 했으므로 이제 이론을 사용하는 방법을 살펴 보겠습니다. HTTP 다이제스트 인증을 구현하려면 필터 체인에서 DigestAuthenticationFilter를 정의해야합니다. 응용 프로그램 컨텍스트는 DigestAuthenticationFilter 및 필수 공동 작업자를 정의해야합니다.

```
<bean id="digestFilter" class=
    "org.springframework.security.web.authentication.www.DigestAuthenticationFilter">
<property name="userDetailsService" ref="jdbcDaoImpl"/>
<property name="authenticationEntryPoint" ref="digestEntryPoint"/>
<property name="userCache" ref="userCache"/>
</bean>

<bean id="digestEntryPoint" class=
    "org.springframework.security.web.authentication.www.DigestAuthenticationEntryPoint">
<property name="realmName" value="Contacts Realm via Digest Authentication"/>
<property name="key" value="acegi"/>
<property name="nonceValiditySeconds" value="10"/>
</bean>
```

DigestAuthenticationFilter는 사용자의 일반 텍스트 비밀번호에 직접 액세스해야하므로 구성된 UserDetailsService가 필요합니다. DAO에서 인코딩 된 비밀번호를 사용하는 경우 다이제스트 인증이 작동하지 않습니다 [9]. DAO 공동 작업자는 UserCache와 함께 일반적으로 DaoAuthenticationProvider와 직접 공유됩니다. DigestAuthenticationFilter가 다이제스트 계산을위한 올바른 realmName 및 키를 얻을 수 있도록 authenticationEntryPoint 특성은 DigestAuthenticationEntryPoint 여야합니다. 
BasicAuthenticationFilter와 마찬가지로 인증에 성공하면 인증 요청 토큰이 SecurityContextHolder에 배치됩니다. 인증 이벤트가 성공했거나 HTTP 헤더에 다이제스트 인증 요청이 없어 인증을 시도하지 않은 경우 필터 체인은 정상적으로 계속 진행됩니다. 필터 체인이 중단되는 유일한 시간은 이전 단락에서 설명한대로 인증이 실패하고 AuthenticationEntryPoint가 호출 된 경우입니다. 
다이제스트 인증의 RFC는 보안을 더욱 강화하기 위해 다양한 추가 기능을 제공합니다. 예를 들어, nonce는 모든 요청마다 변경 될 수 있습니다. 그럼에도 불구하고, 스프링 시큐리티 구현은 구현의 복잡성 (그리고 의심의 여지가없는 사용자 에이전트 비 호환성)을 최소화하고 서버 측 상태를 저장할 필요가 없도록 설계되었습니다. 이러한 기능을 자세히 살펴 보려면 RFC 2617을 검토하십시오. 우리가 아는 한 Spring Security의 구현은 이 RFC의 최소 표준을 준수합니다.

## 10.24 Handling Logouts
### 10.24.1 Logout Java Configuration
WebSecurityConfigurerAdapter를 사용하면 로그 아웃 기능이 자동으로 적용됩니다. 기본적으로 URL / logout에 액세스하면 다음을 통해 사용자가 로그 아웃됩니다.

- HTTP 세션 무효화
- 설정된 RememberMe 인증 정보 삭제
- SecurityContextHolder 삭제
- /login?logout 리다이렉트

그러나 로그인 기능 구성과 유사하게 로그 아웃 요구 사항을 추가로 사용자 정의 할 수있는 다양한 옵션이 있습니다.

```
protected void configure(HttpSecurity http) throws Exception {
    http
        .logout(logout ->                                                       1
            logout
                .logoutUrl("/my/logout")                                        2
                .logoutSuccessUrl("/my/index")                                  3
                .logoutSuccessHandler(logoutSuccessHandler)                     4
                .invalidateHttpSession(true)                                    5
                .addLogoutHandler(logoutHandler)                                6
                .deleteCookies(cookieNamesToClear)                              7
        )
        ...
}
```

1. 로그 아웃 지원을 제공합니다. WebSecurityConfigurerAdapter를 사용할 때 자동으로 적용됩니다.
2. 로그 아웃을 트리거하는 URL(기본값은 /logout). CSRF 보호가 활성화 된 경우 (기본값) 요청도 POST 여야합니다. 자세한 정보는 JavaDoc을 참조하십시오.
3. 로그 아웃 후 리디렉션 할 URL입니다. 기본값은 /login?logout입니다. 자세한 정보는 JavaDoc을 참조하십시오.
4. 사용자 정의 LogoutSuccessHandler를 지정하겠습니다. 이를 지정하면 logoutSuccessUrl()이 무시됩니다. 자세한 정보는 JavaDoc을 참조하십시오.
5. 로그 아웃시 HttpSession을 무효화할지 여부를 지정하십시오. 기본적으로 적용됩니다. 표지 아래에 SecurityContextLogoutHandler를 구성합니다. 자세한 정보는 JavaDoc을 참조하십시오.
6. LogoutHandler를 추가합니다. SecurityContextLogoutHandler는 기본적으로 마지막 LogoutHandler로 추가됩니다.
7. 로그 아웃 성공시 쿠키 이름 지정을 제거 할 수 있습니다. 이것은 CookieClearingLogoutHandler를 명시적으로 추가하기위한 바로 가기입니다.

> === 로그 아웃은 물론 XML 네임 스페이스 표기법을 사용하여 구성 할 수도 있습니다. 자세한 내용은 Spring Security XML 네임 스페이스 섹션에서 로그 아웃 요소에 대한 문서를 참조하십시오. ===

일반적으로 로그 아웃 기능을 사용자 정의하기 위해 LogoutHandler와 LogoutSuccessHandler를 함께 또는 각각 추가 할 수 있습니다. 많은 일반적인 시나리오에서 유창한 API를 사용할 때 이러한 핸들러가 적용됩니다.

### 10.24.2 Logout XML Configuration
logout 요소는 특정 URL로 이동하여 로그 아웃 지원을 추가합니다. 기본 로그 아웃 URL은 /logout이지만 logout-url 속성을 사용하여 다른 것으로 설정할 수 있습니다. 사용 가능한 다른 속성에 대한 자세한 내용은 네임 스페이스 부록에서 찾을 수 있습니다.

### 10.24.3 LogoutHandler
일반적으로 LogoutHandler 구현은 로그 아웃 처리를 할 수있는 클래스를 나타냅니다. 정리가 필요한 작업을 수행하기 위해 호출 될 것으로 예상됩니다. 따라서 예외를 던져서는 안됩니다. 다양한 구현이 제공됩니다.

- PersistentTokenBasedRememberMeServices
- TokenBasedRememberMeServices
- CookieClearingLogoutHandler
- CsrfLogoutHandler
- SecurityContextLogoutHandler
- HeaderWriterLogoutHandler

자세한 내용은 10.13.4 절. “Remember-Me Interfaces and Implementations”을 참조하십시오.
몇몇 유명한 API는 LogoutHandler 구현을 직접 제공하는 대신 구체적인 LogoutHandler 구현체를 사용할 수 있는 지름길도 제공합니다. 예를들어, deleteCookies()를 사용하면 로그 아웃 시 제거 할 하나 이상의 쿠키 이름을 지정할 수 있습니다. 이것은 CookieClearingLogoutHandler를 추가하는 것과 비교하면 간단한 작업입니다.

### 10.24.4 LogoutSuccessHandler
LogoutSuccessHandler는 LogoutFilter에 의해 성공적으로 로그 아웃한 후 호출됩니다. 이 핸들러는 예를 들어 적절한 목적지로의 재전송 또는 전달 같은 후처리를 위해 사용됩니다. 인터페이스는 LogoutHandler와 거의 동일하지만 예외가 발생할 수 있습니다.
다음과 같은 구현이 제공됩니다.

- SimpleUrlLogoutSuccessHandler
- HttpStatusReturningLogoutSuccessHandler

위에서 언급했듯이 SimpleUrlLogoutSuccessHandler를 직접 지정할 필요가 없습니다. 대신, API는 logoutSuccessUrl()을 설정하여 지름길을 제공합니다. 이것은 구체적으로 SimpleUrlLogoutSuccessHandler를 설정합니다. 제공된 URL은 로그 아웃이 발생한 후 리디렉션됩니다. 기본값은 /login?logout입니다.

HttpStatusReturningLogoutSuccessHandler는 REST API 유형 시나리오에서 흥미로울 수 있습니다. 성공적인 로그 아웃 시 URL로 리디렉션하는 대신 이 LogoutSuccessHandler를 사용하면 일반 HTTP 상태 코드를 제공 할 수 있습니다. 구성되지 않은 경우 기본적으로 상태 코드 200이 반환됩니다.

### 10.24.5 Further Logout-Related References
- Logout Handling
- Testing Logout
- HttpServletRequest.logout()
- Section 10.13.4, “Remember-Me Interfaces and Implementations”
- Logging Out in section CSRF Caveats
- Section Single Logout (CAS protocol)
- Documentation for the logout element in the Spring Security XML Namespace section

### 10.25 Setting a Custom AuthenticationEntryPoint
네임스페이스를 통해 form 로그인, OpenID 또는 basic authenticaction을 사용하지 않고, 기존 Bean 구문을 사용하여 인증 필터 및 진입점(EntoryPoint)을 정의하고 앞에서 본 것처럼 네임스페이스에 링크 할 수 있습니다. <http> 요소의 entry-point-ref 속성을 사용하여 해당 AuthenticationEntryPoint를 설정할 수 있습니다.
CAS 샘플 애플리케이션은이 구문을 포함하여 네임 스페이스와 함께 사용자 정의 Bean을 사용하는 좋은 예입니다. 인증 진입 점에 익숙하지 않은 경우 기술 개요 장에서 설명합니다.







