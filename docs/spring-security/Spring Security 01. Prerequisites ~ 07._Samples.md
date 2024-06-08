# I. Preface

이 문서는 스프링 시큐리티의 로직을 다룹니다.

# 1. Prerequisites
스프링 시큐리티는 자바 8 또는 그 이상 버전을 요구합니다.
스프링 시큐리티는 자체적으로 동작하는 것을 지향하기 때문에 특정 경로에 설정 파일이나 환경을 요구하지 않습니다. 특히 자바 인증과 권한 서비스를 위한 정책 파일이나 스프링 시큐리티를 위한 파일 등을 자바 클래스패스 등에 위치시키지 않아도 됩니다.
당신이 EJB 컨테이너나 서블릿 컨테이너를 사용할 경우에도 설정 파일을 서버 클래스 로더에 위치시키지 않아도 됩니다. 모든 필요한 파일은 작성한 어플리케이션에 포함되어 있습니다.
이 디자인은 배포 시간의 유연성을 제공합니다.

# 2. Spring Security Comunity
스프링 시큐리티 커뮤니티에 오신것을 환영합니다. 이 섹션에서는 방대한 커뮤니티를 최대한 활용하는 방법에 대해 설명합니다.

## 2.1 Getting Help
Spring Security에 대한 도움이 필요한 경우 여기에서 도움을 얻을 수 있습니다. 다음은 도움을 얻는 가장 좋은 방법입니다.
- 이 문서를 읽으세요.
- sample applications을 사용해보세요.
- 스택오버플로우에 spring-security 태그를 달아서 질문을 올리세요.
- https://github.com/spring-projects/spring-security/issues에 버그 리포트와 수정 요청을 올리세요.

## 2.2 Becoming Involved
Spring Security 프로젝트에 참여하신 것을 환영합니다. StackOverflow에 대한 질문에 답하기, 새 코드 작성, 기존 코드 개선, 문서 지원, 샘플 또는 자습서 개발, 버그보고 또는 제안 제안 등 여러 가지 방법으로 기여할 수 있습니다. 자세한 내용은 기여 문서를 참조하십시오.

## 2.3 Source Code
https://github.com/spring-projects/spring-security/ 에서 소스코드를 받을 수 있습니다.

## 2.4 Apache 2 License
스프링 시큐리티는 Apache 2.0 라이선스로 배포됩니다.

## 2.5 Social Media
트위터에서 @SpringSecurity 및 Spring Security 팀을 팔로우하여 최신 뉴스를 확인할 수 있습니다. @SpringCentral을 팔로우하여 전체 Spring 포트폴리오를 최신 상태로 유지할 수 있습니다.


# 3. 생략

# 4. Getting Spring Security
이 섹션에서는 Spring Security 바이너리를 얻는 데 필요한 모든 것을 설명합니다. 소스 코드를 얻는 방법은 2.3 절.“소스 코드”를 참조하십시오.

## 4.1 Release Numbering
Spring Security 버전은 다음과 같이 MAJOR.MINOR.PATCH로 형식화됩니다.
- MAJOR 버전에는 주요 변경 사항이 포함될 수 있습니다. 일반적으로 최신 보안 관행에 맞게 향상된 보안을 제공하기 위해 수행됩니다. 
- MINOR 버전에는 향상된 기능이 포함되어 있지만 수동 업데이트로 간주됩니다. 
- 패치 수준을 수정하는 변경 사항을 제외하고 패치 수준은 앞뒤로 완벽하게 호환되어야합니다.

## 4.2 Usage with Maven
대부분의 오픈 소스 프로젝트 인 Spring Security는 종속성을 Maven 아티팩트로 배포합니다. 이 섹션의 주제는 Maven을 사용할 때 Spring Security를 ​​사용하는 방법에 대한 세부 사항을 제공합니다.

## 4.2.1 Spring Boot with Maven
스프링 부트는 spring-boot-starter-security를 제공하여 spring-security 관련 의존성을 하나로 통합해서 제공합니다. 스타터를 사용하는 가장 간단하고 선호되는 방법은 IDE 통합 (Eclipse, IntelliJ, NetBeans) 또는 https://start.spring.io를 통해 Spring Initializr를 사용하는 것입니다.

**Example 4.1. pom.xml**
```
<dependencies>
    <!-- ... other dependency elements ... -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
</dependencies>
```

추가 기능 (예 : LDAP, OpenID 등)을 사용하는 경우 6 장 프로젝트 모듈의 내용도 포함해야합니다.

## 4.2.2 Maven Without Spring Boot
Spring Boot없이 Spring Security를 ​​사용하는 경우 선호되는 방법은 Spring Security의 BOM을 사용하여 전체 프로젝트에서 일관된 Spring Security 버전을 사용하는 것입니다. 다음 예제는 이를 수행하는 방법을 보여줍니다.

**Example 4.4. pom.xml**
```
<dependencyManagement>
    <dependencies>
        <!-- ... other dependency elements ... -->
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-bom</artifactId>
            <version>5.2.1.RELEASE</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Spring Security Maven의 최소한의 종속성 세트는 일반적으로 다음과 같습니다.

**Example 4.5. pom.xml**
```
<dependencies>
    <!-- ... other dependency elements ... -->
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-config</artifactId>
    </dependency>
</dependencies>
```

추가 기능 (예 : LDAP, OpenID 등)을 사용하는 경우 6 장 프로젝트 모듈의 내용도 포함해야합니다.

Spring Security는 Spring Framework 5.2.1.RELEASE에 대해 빌드되지만 일반적으로 최신 버전의 Spring Framework 5.x에서도 작동합니다. 많은 사용자들이 스프링 시큐리티의 전이 의존성이 Spring Framework 5.2.1.RELEASE에서 이상한 클래스 경로 문제를 발생시키는 것을 두려워 합니다. 이를 해결하는 가장 쉬운 방법은 다음 예제와 같이 pom.xml의 <dependencyManagement> 섹션에서 spring-framework-bom을 사용하는 것입니다.

**Example 4.6. pom.xml**
```
<dependencyManagement>
    <dependencies>
        <!-- ... other dependency elements ... -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-framework-bom</artifactId>
            <version>5.2.1.RELEASE</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

앞의 예제는 Spring Security의 모든 전이 종속성이 Spring 5.2.1.RELEASE 모듈을 사용하도록합니다.

> 이 방법은 Maven의 "BOM (bill of materials)"개념을 사용하며 Maven 2.0.9 이상에서만 사용할 수 있습니다. 종속성 해결 방법에 대한 자세한 내용은 Maven의 종속성 메커니즘 소개 설명서를 참조하십시오.

## 4.2.3 Maven Repositories
모든 GA 릴리스 (즉, .RELEASE로 끝나는 버전)는 Maven Central에 배포되므로 추가 Maven 리포지토리를 pom에 선언 할 필요가 없습니다.
SNAPSHOT 버전을 사용하는 경우 다음 예제와 같이 Spring Snapshot 저장소가 정의되어 있는지 확인해야합니다.

**Example 4.7. pom.xml**
```
<repositories>
    <!-- ... possibly other repository elements ... -->
    <repository>
        <id>spring-snapshot</id>
        <name>Spring Snapshot Repository</name>
        <url>https://repo.spring.io/snapshot</url>
    </repository>
</repositories>
```

마일스톤 또는 릴리스 후보 버전을 사용하는 경우 다음 예제와 같이 스프링 마일스톤 저장소가 정의되어 있는지 확인해야합니다.

**Example 4.8. pom.xml**
```
<repositories>
    <!-- ... possibly other repository elements ... -->
    <repository>
        <id>spring-milestone</id>
        <name>Spring Milestone Repository</name>
        <url>https://repo.spring.io/milestone</url>
    </repository>
</repositories>
```

## 4.3 Gradle
생략

# 5. Features
Spring Security는 인증, 권한 부여 및 일반적인 취약점에 대한 보호를 포괄적으로 지원합니다. 또한 다른 라이브러리와 통합하여 사용을 단순화합니다.

## 5.1 Protection Against Exploits
Spring Security는 일반적인 취약점으로부터 보호합니다. 가능한 경우, 보호 기능은 디폴트 입니다. 다음은 Spring Security가 보호하는 다양한 취약점에 대한 높은 수준의 설명입니다.

### 5.1.1 Cross Site Request Forgery (CSRF)
Spring은 CSRF (Cross Site Request Forgery) 공격으로부터 보호하기위한 포괄적 인 지원을 제공합니다. 다음 섹션에서 살펴볼 것입니다.
-"CSRF 공격이란 무엇입니까?"
-"CSRF 공격 방지"
-"CSRF 고려 사항"

>이 문서 부분에서는 CSRF 보호의 일반적인 주제에 대해 설명합니다. 서블릿 및 WebFlux 기반 애플리케이션의 CSRF 보호에 대한 특정 정보는 관련 섹션을 참조하십시오.

###What is a CSRF Attack?

CSRF 공격을 이해하는 가장 좋은 방법은 구체적인 예를 살펴 보는 것입니다.
은행 웹 사이트가 현재 로그인 한 사용자에서 다른 은행 계좌로 송금 할 수있는 양식을 제공한다고 가정합니다. 예를 들어, 전송 양식은 다음과 같습니다.

**Example 5.1. Transfer form**
```
<form method="post"
    action="/transfer">
<input type="text"
    name="amount"/>
<input type="text"
    name="routingNumber"/>
<input type="text"
    name="account"/>
<input type="submit"
    value="Transfer"/>
</form>
```

해당 HTTP 요청은 다음과 같습니다.

**Example 5.2. Transfer HTTP request**
```
POST /transfer HTTP/1.1
Host: bank.example.com
Cookie: JSESSIONID=randomid
Content-Type: application/x-www-form-urlencoded

amount=100.00&routingNumber=1234&account=9876
```

이제 은행 웹 사이트를 인증 한 다음 로그 아웃하지 않고 악의적인 웹 사이트를 방문하십시오. 사악한 웹 사이트에는 다음과 같은 형식의 HTML 페이지가 있습니다.

**Example 5.3. Evil transfer form**
```
<form method="post"
    action="https://bank.example.com/transfer">
<input type="hidden"
    name="amount"
    value="100.00"/>
<input type="hidden"
    name="routingNumber"
    value="evilsRoutingNumber"/>
<input type="hidden"
    name="account"
    value="evilsAccountNumber"/>
<input type="submit"
    value="Win Money!"/>
</form>
```

당신이 "Win Money!"라는 문구를 보고 submit 버튼을 클릭하면 100달러가 해커에게 송금될 것입니다. 이것은 악의적인 웹사이트가 당신의 쿠키(cookies)를 보지는 못하지만 은행과 관련된 쿠키는 요청과 함께 악의적인 웹 사이트로 전송되기 때문입니다.

더 안 좋은 것은, 이 모든 과정이 자바스크립트로 자동화되어 실행될 수 있다는 것입니다. 이 말은 당신이 버튼을 클릭하지 않아도 위와 같은 작업이 가능하다는 이야기 입니다. 또한, XSS 공격에 당한 정직한/정상적인 웹사이트를 방문했을 경우에도 쉽게 일어날 수 있습니다. 그렇다면 이런 공격으로부터 사용자를 보호하는 방법에는 어떤 것이 있을까요?

### Protecting Against CSRF Attacks
CSRF 공격이 가능한 이유는 피해자의 웹사이트에서 보내는 HTTP 요청과 공격자의 웹사이트에서 보내는 HTTP 요청이 정확히 같기 때문입니다. 즉, 악의적인 웹사이트에서 오는 요청을 거부하고 정상적인 은행 웹사이트에서 오는 요청을 허용 할 방법이 없습니다. CSRF 공격을 방어하기 위해선 악의적인 웹사이트에서 제공할 수 없는 정보를 식별하여 두 요청을 구분하는 방법 밖에는 없습니다.

Spring은 두가지 메커니즘을 통해 CSRF 공격을 방어합니다.

- “Synchronizer Token Pattern”
- 세션 쿠기의 “SameSite Attribute”

>Both protections require require that the section called “Safe Methods Must be Idempotent”

### Safe Methods Must be Idempotent
CSRF에 대한 보호 기능이 작동하려면 응용 프로그램은 "안전한"HTTP 메소드가 멱등성을 제공하는지 확인해야합니다. 이는 HTTP 메소드 GET, HEAD, OPTIONS 및 TRACE를 사용하는 요청이 애플리케이션의 상태를 변경하지 않아야 함을 의미합니다.

### Synchronizer Token Pattern
CSRF 공격으로부터 보호하는 가장 광범위하고 포괄적인 방법은 Synchronizer Token Pattern을 사용하는 것입니다. 이 솔루션은 세션 쿠키 외에도 각 HTTP 요청에 CSRF 토큰이라는 안전한 임의 생성 값이 HTTP 요청에 있어야합니다.

HTTP 요청이 제출되면 서버는 제공되어야할 CSRF 토큰과 HTTP 요청의 CSRF 토큰을 비교합니다. 토큰 값이 일치하지 않을 경우 HTTP 요청은 거부됩니다.
이 작업의 핵심은 실제 CSRF 토큰이 HTTP 요청의 일부여야한다는 것이고, 브라우저에 의해 자동으로 추가하는 값이 아니어야 한다는 것입니다. 예를들어, HTTP 매개 변수 또는 HTTP 헤더에 CSRF 토큰을 요구하면 CSRF 공격으로부터 보호됩니다. 쿠키에 포함할 경우에는 브라우저에 의해 HTTP 요청에 자동으로 포함되므로 작동하지 않습니다.

애플리케이션 상태를 업데이트하는 각 HTTP 요청에 대해 실제 CSRF 토큰 만 요구한다는 기대를 완화 할 수 있습니다. 이를 위해서는 애플리케이션에서 안전한 HTTP 메소드가 멱등성을 지원하는지 확인해야합니다. 외부 사이트의 링크를 사용하여 웹 사이트에 링크를 허용하기 때문에 사용성이 향상됩니다. 또한 토큰이 유출 될 수 있으므로 HTTP GET에 임의 토큰을 포함시키지 않으려고 합니다.

Synchronizer Token Pattern을 사용할 때 예제가 어떻게 변경되는지 살펴 보겠습니다. 실제 CSRF 토큰이 _csrf라는 HTTP 매개 변수에 있어야한다고 가정하십시오. 신청서의 이체 양식은 다음과 같습니다.

**Example 5.4. Synchronizer Token Form**
```
<form method="post"
    action="/transfer">
<input type="hidden"
    name="_csrf"
    value="4bfd1575-3ad1-4d21-96c7-4ef2d9f86721"/>
<input type="text"
    name="amount"/>
<input type="text"
    name="routingNumber"/>
<input type="hidden"
    name="account"/>
<input type="submit"
    value="Transfer"/>
</form>
```

이 양식에는 이제 CSRF 토큰 값을 가진 숨겨진 입력이 포함됩니다. 동일한 원본 정책으로 인해 악의적 인 사이트가 응답을 읽을 수 없으므로 외부 사이트가 CSRF 토큰을 읽을 수 없습니다.
송금을 위한 해당 HTTP 요청은 다음과 같습니다.

**Example 5.5. Synchronizer Token request**
```
POST /transfer HTTP/1.1
Host: bank.example.com
Cookie: JSESSIONID=randomid
Content-Type: application/x-www-form-urlencoded

amount=100.00&routingNumber=1234&account=9876&_csrf=4bfd1575-3ad1-4d21-96c7-4ef2d9f86721
```

이제 HTTP 요청에 안전한 임의 값을 가진 _csrf 매개변수가 포함되어 있습니다. 사악한 웹사이트는 _csrf 매개변수에 올바른 값을 제공할 수 없습니다.(사악한 웹 사이트에서 명시적으로 제공해야 함) submit 버튼을 클릭하면 서버에서 실제 CSRF토큰을 서버의 CSRF토큰과 비교할 것이고 요청은 실패처리될 것입니다.


### SameSite Attribute
CSRF 공격으로부터 보호하는 새로운 방법은 쿠키에 SameSite 속성을 지정하는 것입니다. 쿠키를 설정할 때 서버는 SameSite 속성을 지정하여 외부 사이트에서 올 때 쿠키를 보내지 않아야 함을 나타냅니다.

> 스프링 시큐리티는 세션 쿠키 생성을 직접 제어하지 않으므로 SameSite 속성을 지원하지 않습니다. 스프링 세션은 서블릿 기반 애플리케이션에서 SameSite 속성을 지원합니다. Spring Framework의 CookieWebSessionIdResolver는 WebFlux 기반 애플리케이션에서 SameSite 속성을 즉시 지원합니다.

예를 들어, SameSite 속성을 가진 HTTP 응답 헤더는 다음과 같습니다.

**Example 5.6. SameSite HTTP response**
```
Set-Cookie: JSESSIONID=randomid; Domain=bank.example.com; Secure; HttpOnly; SameSite=Lax
```

SameSite 속성의 유효한 값은 다음과 같습니다.
- Strict - 동일한 사이트에서 들어오는 모든 요청에 지정된 경우 쿠키가 포함됩니다. 그렇지 않으면, 쿠키가 HTTP 요청에 포함되지 않습니다.
- Lax - 동일 사이트에서 올 때 또는 최상위 탐색이며 메서드가 멱등성일 때 쿠키가 전송됩니다. 그렇지 않으면 쿠키가 HTTP 요청에 포함되지 않습니다.

예제를 통해 SameSite 속성을 사용하여 보호하는 방법을 살펴 보겠습니다. 은행 애플리케이션은 세션 쿠키에 SameSite 속성을 지정하여 CSRF로부터 보호 할 수 있습니다.
세션 쿠키에 SameSite 속성이 설정되어 있으면, 브라우저는 은행 웹사이트에서 오는 요청과 함께 JSESSIONID 쿠키를 계속 보냅니다. 그러나 브라우저는 더 이상 악의적인 웹사이트에서 온 송금 요청과 함께 JSESSIONID 쿠키를 보내지 않습니다. 악의적인 웹사이트에서 오는 전송 요청에 세션이 더 이상 존재하지 않기 때문에 응용 프로그램은 CSRF 공격으로부터 보호됩니다.

CSRF 공격으로부터 보호하기 위해 SameSite 속성을 사용할 때 알아야 할 몇 가지 중요한 고려 사항이 있습니다.

SameSite 속성을 Strict로 설정하면 더 강력한 방어 기능을 제공하지만 사용자를 혼동 할 수 있습니다. https://social.example.com에서 호스팅되는 소셜 미디어 사이트에 로그인 한 사용자를 고려하십시오. 사용자는 https://email.example.org에서 소셜 미디어 사이트에 대한 링크가 포함 된 이메일을받습니다. 사용자가 링크를 클릭하면 소셜 미디어 사이트에 대한 인증이 정당하게 이루어집니다. 그러나 SameSite 속성이 Strict이면 쿠키가 전송되지 않으므로 사용자가 인증되지 않습니다.

>gh-7537을 구현하여 CSRF 공격에 대한 SameSite 보호의 보호 및 사용성을 향상시킬 수 있습니다.

또 다른 확실한 고려 사항은 SameSite 특성이 사용자를 보호하기 위해 브라우저가 SameSite 특성을 지원해야한다는 것입니다. 대부분의 최신 브라우저는 SameSite 속성을 지원합니다. 그러나 여전히 사용중인 이전 브라우저는 그렇지 않을 수 있습니다.
따라서 일반적으로 CSRF 공격에 대한 유일한 보호보다는 SameSite 특성을 심층 방어로 사용하는 것이 좋습니다.

### When to use CSRF protection
언제 CSRF 보호를 사용해야합니까? 일반 사용자가 브라우저에서 처리 할 수있는 모든 요청에 CSRF 보호를 사용하는 것이 좋습니다. 브라우저 이외의 클라이언트가 사용하는 서비스 만 만드는 경우 CSRF 보호를 사용하지 않을 수 있습니다.

### CSRF protection and JSON
일반적인 질문은 "자바 스크립트로 작성된 JSON 요청을 보호해야합니까?"입니다. 짧은 대답은, "경우에 따라 다릅니다" 입니다. 그러나 JSON 요청에 영향을 줄 수있는 CSRF 악용이 있으므로 매우 주의해야합니다. 예를 들어 악의적인 사용자는 다음 형식을 사용하여 JSON으로 CSRF를 만들 수 있습니다.

**Example 5.7. CSRF with JSON form**
```
<form action="https://bank.example.com/transfer" method="post" enctype="text/plain">
    <input name='{"amount":100,"routingNumber":"evilsRoutingNumber","account":"evilsAccountNumber", "ignore_me":"' value='test"}' type='hidden'>
    <input type="submit"
        value="Win Money!"/>
</form>
```

이것은 다음 JSON 구조를 생성합니다

**Example 5.8. CSRF with JSON request**
```
{ "amount": 100,
"routingNumber": "evilsRoutingNumber",
"account": "evilsAccountNumber",
"ignore_me": "=test"
}
```

응용 프로그램이 Content-Type의 유효성을 검사하지 않을 경우이 취약점에 노출됩니다. 설정에 따라 Content-Type의 유효성을 검사하는 Spring MVC 애플리케이션은 아래와 같이 URL 접미 부를 .json으로 끝나도록 업데이트하여 여전히 악용 될 수 있습니다.

**Example 5.9. CSRF with JSON Spring MVC form**
```
<form action="https://bank.example.com/transfer.json" method="post" enctype="text/plain">
    <input name='{"amount":100,"routingNumber":"evilsRoutingNumber","account":"evilsAccountNumber", "ignore_me":"' value='test"}' type='hidden'>
    <input type="submit"
        value="Win Money!"/>
</form>
```

### CSRF and Stateless Browser Applications
stateless 어플리케이션인 경우 어떻게합니까? 그렇다고 반드시 보호되고 있다는 의미는 아닙니다. 실제로 사용자가 특정 요청에 대해 웹 브라우저에서 작업을 수행 할 필요가없는 경우에도 CSRF 공격에 취약 할 수 있습니다.
예를 들어, JSESSIONID 대신 인증을 위해 쿠키 내에 모든 상태를 포함하는 사용자 정의 쿠키를 사용하는 애플리케이션을 고려하십시오. CSRF 공격이 이루어지면 이전 예제에서 JSESSIONID 쿠키가 전송 된 것과 동일한 방식으로 사용자 지정 쿠키가 요청과 함께 전송됩니다. 이 응용 프로그램은 CSRF 공격에 취약합니다.
기본 인증을 사용하는 응용 프로그램도 CSRF 공격에 취약합니다. 브라우저는 이전 예제에서 JSESSIONID 쿠키가 전송 된 것과 동일한 방식으로 요청에 사용자 이름과 비밀번호를 자동으로 포함하므로 애플리케이션이 취약합니다.

### CSRF Considerations
CSRF 공격에 대한 보호를 구현할 때 고려해야 할 몇 가지 특별한 고려 사항이 있습니다.

### Logging In
로그인 요청 위조를 방지하려면 HTTP 요청의 로그인을 CSRF 공격으로부터 보호해야합니다. 악의적인 사용자가 피해자의 민감한 정보를 읽을 수 없도록 로그인 요청 위조를 방지해야합니다. 공격은 다음에 의해 실행됩니다.
- 악의적인 사용자가 악의적인 사용자의 자격 증명을 사용하여 CSRF 로그인을 수행합니다. 피해자는 이제 악의적인 사용자로 인증됩니다.
- 그런 다음 악의적인 사용자는 피해자가 손상된 웹사이트를 방문하여 민감한 정보를 입력하도록 속입니다
- 이 정보는 악의적인 사용자의 계정과 연결되어 있으므로 악의적인 사용자는 자신의 자격 증명으로 로그인하여 피해자의 민감한 정보를 볼 수 있습니다
방어를 위한 방법은 아래 CSRF and Session Timeouts을 참조하세요.

### Logging Out
로그 아웃 요청이 위조되지 않도록 하려면 로그 아웃 HTTP 요청을 CSRF 공격으로부터 보호해야합니다. 악의적인 사용자가 피해자의 민감한 정보를 읽을 수 없도록 로그 아웃 요청을 위조하지 않아야합니다. 

### CSRF and Session Timeouts
예상되는 CSRF 토큰은 종종 세션에 저장됩니다. 이는 세션이 만료되면 서버가 예상 CSRF 토큰을 찾지 못하고 HTTP 요청을 거부함을 의미합니다. 각각의 트레이드 오프와 함께 Session Timeout을 해결하기위한 여러 가지 옵션이 있습니다.
- Session Timeout를 완화하는 가장 좋은 방법은 JavaScript를 사용하여 양식 제출 시 CSRF 토큰을 요청하는 것입니다. 그런 다음 양식이 CSRF 토큰으로 업데이트되어 제출됩니다.
- 또 다른 옵션은 JavaScript를 사용하여 사용자에게 세션이 만료 될 예정임을 알리는 것입니다. 사용자는 버튼을 클릭하여 세션을 유지하고 refresh할 수 있습니다.
- 마지막으로, 예상 CSRF 토큰은 쿠키에 저장될 수 있습니다. 이를 통해 예상 CSRF 토큰이 세션보다 오래 지속될 수 있습니다.
예상 CSRF 토큰이 기본적으로 쿠키에 저장되지 않는지 물을 수 있습니다. 이것은, 다른 도메인에서 헤더(예: 쿠키 지정)를 설정할 수 있는 알려진 취약점이 있기 때문입니다. 헤더에 X-Requested-With가 있을 경우 Ruby on Rails가 더 이상 CSRF 검사를 건너 뛰지 않는 것과 같은 이유입니다. 취약점에 대한 자세한 내용은이 webappsec.org 스레드를 참조하십시오. 또 다른 단점은 상태(예: 시간초과)를 제거하면 토큰이 탈취(손상, compromised)될 경우에 강제로 토큰을 만료시킬 수 없다는 점입니다.

### Multipart (file upload)
CSRF 공격으로부터 멀티 파트 요청(파일 업로드)을 보호하려 하면 닭과 계란 문제가 발생합니다. CSRF 공격이 발생하지 않도록하려면 실제 CSRF 토큰을 얻기 위해 HTTP 요청 본문을 읽어야합니다. 그러나 본문을 읽으면 파일이 업로드되므로 외부 사이트에서 파일을 업로드 할 수 있습니다.
multipart / form-data와 함께 CSRF 보호를 사용하는 데는 두 가지 옵션이 있습니다. 각 옵션에는 장단점이 있습니다.

- Place CSRF Token in the Body
- Place CSRF Token in the URL

> Spring Security의 CSRF 보호 기능을 멀티 파트 파일 업로드와 통합하기 전에 먼저 CSRF 보호없이 업로드 할 수 있는지 확인하십시오. Spring에서 멀티 파트 폼을 사용하는 것에 대한 자세한 정보는 Spring 레퍼런스의 1.1.11 Multipart Resolver 섹션과 MultipartFilter javadoc에서 찾을 수 있습니다. 

### Place CSRF Token in the Body
첫 번째 옵션은 요청 본문에 실제 CSRF 토큰을 포함시키는 것입니다. 본문에 CSRF 토큰을 배치하면 권한 부여를 수행하기 전에 본문을 읽습니다. 즉, 누구나 서버에 임시 파일을 배치 할 수 있습니다. 그러나 승인된 사용자만 응용 프로그램에 파일을 넘길 수 있습니다. 일반적으로 이 방법을 추천합니다. 임시 파일 업로드는 대부분의 서버에서 무시할만한 영향 밖엔 없습니다.

### Include CSRF Token in URL
권한이 없는 사용자가 임시 파일을 업로드하도록 허용할 수 없는 경우, 예상 CSRF 토큰을 쿼리 파라미터로 만들어서 폼의 속성 정보로 포함시키는 방법이 있습니다.(URL에 토큰을 포함해서 ?token="" 형식으로 전송하는 방법) 이 방법의 단점은 쿼리 매개변수가 유출 될 수 있다는 것입니다. 보다 일반적으로 기밀 정보를 본문이나 헤더 내에 배치하여 유출되지 않도록하는 것이 가장 좋습니다. 추가 정보는 RFC 2616 Section 15.1.3 Encoding Sensitive Information in URI’s 에서 찾을 수 있습니다.

### HiddenHttpMethodFilter
일부 애플리케이션에서는 양식 매개 변수를 사용하여 HTTP 메소드를 대체 할 수 있습니다. 예를 들어, 아래처럼 POST HTTP 메소드를 DELETE처럼 사용할 수 있습니다.

**Example 5.10. CSRF Hidden HTTP Method Form**
```
<form action="/process"
    method="post">
    <!-- ... -->
    <input type="hidden"
        name="_method"
        value="delete"/>
</form>
```
HTTP 메소드 오버라이드는 필터에서 발생합니다. 해당 필터는 Spring Security 전에 배치해야합니다. 오버라이드는 post에서만 발생하므로 실제 문제는 거의 발생하지 않습니다. 그러나 Spring Security의 필터 앞에 배치하는 것이 가장 좋습니다.

# 6. Project Modules
Spring Security 3.0에서 코드베이스는 서로 다른 기능 영역과 타사 종속성을 더 명확하게 구분하는 별도의 jar로 세분화되었습니다. Maven을 사용하여 프로젝트를 빌드하는 경우 pom.xml에 추가해야하는 모듈입니다. Maven을 사용하지 않더라도 타사 종속성 및 버전에 대한 아이디어를 얻으려면 pom.xml 파일을 참조하는 것이 좋습니다. 또 다른 좋은 아이디어는 샘플 응용 프로그램에 포함 된 라이브러리를 검사하는 것입니다.

## 6.1 Core — spring-security-core.jar
이 모듈에는 핵심 인증 및 액세스 제어 클래스 및 인터페이스, 원격 지원 및 기본 프로비저닝 API가 포함되어 있습니다. Spring Security를 사용하는 모든 애플리케이션에 필요합니다. 독립형 애플리케이션, 원격 클라이언트, 메소드 (서비스 계층) 보안 및 JDBC 사용자 프로비저닝을 지원합니다. 다음과 같은 최상위 패키지가 포함되어 있습니다.

- org.springframework.security.core
- org.springframework.security.access
- org.springframework.security.authentication
- org.springframework.security.provisioning

## 6.2 Remoting — spring-security-remoting.jar
이 모듈은 Spring Remoting과의 통합을 제공합니다. Spring Remoting을 사용하는 원격 클라이언트를 작성하지 않는 한 이것을 필요로하지 않습니다. 기본 패키지는 org.springframework.security.remoting입니다.

## 6.3 Web — spring-security-web.jar
이 모듈에는 필터 및 관련 웹 보안 인프라 코드가 포함되어 있습니다. 서블릿 API 종속성이있는 항목이 포함되어 있습니다. Spring Security 웹 인증 서비스 및 URL 기반 액세스 제어가 필요한 경우 필요합니다. 기본 패키지는 org.springframework.security.web입니다.

## 6.4 Config — spring-security-config.jar
이 모듈에는 security namespace parsing code 및 Java configuration 코드가 포함되어 있습니다. Spring Security의 Java Configuratin 지원을 사용하거나 설정을 위해 Spring Security XML namespace를 사용하는 경우 필요합니다. 기본 패키지는 org.springframework.security.config입니다. 어떤 클래스도 응용 프로그램에서 직접 사용할 수 없습니다.

## 6.5 LDAP — spring-security-ldap.jar
이 모듈은 LDAP 인증 및 프로비저닝 코드를 제공합니다. LDAP 인증을 사용하거나 LDAP으로 사용자 항목을 관리해야하는 경우 필요합니다. 최상위 패키지는 org.springframework.security.ldap입니다.

## 6.6 OAuth 2.0 Core — spring-security-oauth2-core.jar
spring-security-oauth2-core.jar에는 OAuth 2.0 인증 프레임 워크 및 OpenID Connect Core 1.0을 지원하는 핵심 클래스 및 인터페이스가 포함되어 있습니다. 클라이언트, 리소스 서버 및 권한 부여 서버와 같은 OAuth 2.0 또는 OpenID Connect Core 1.0을 사용하는 응용 프로그램에 필요합니다. 최상위 패키지는 org.springframework.security.oauth2.core입니다.

## 6.7 OAuth 2.0 Client — spring-security-oauth2-client.jar
spring-security-oauth2-client.jar에는 OAuth 2.0 인증 프레임 워크 및 OpenID Connect Core 1.0에 대한 Spring Security의 클라이언트 지원이 포함되어 있습니다. OAuth 2.0 로그인 또는 OAuth 클라이언트 지원을 사용하는 응용 프로그램에 필요합니다. 최상위 패키지는 org.springframework.security.oauth2.client입니다.

## 6.8 OAuth 2.0 JOSE — spring-security-oauth2-jose.jar
spring-security-oauth2-jose.jar에는 Spring Security에서 제공하는 JOSE(Javascript Object Signing and Encryption) 프레임워크가 포함되어 있습니다. JOSE 프레임워크는 파티(parties)간 요청사항을 안전하게 전달하는 방법을 제공하기위한 것입니다. 이 모듈은 아래 모듈들을 이용해 빌드됩니다.
- JSON Web Token (JWT)
- JSON Web Signature (JWS)
- JSON Web Encryption (JWE)
- JSON Web Key (JWK)

다음과 같은 최상위 패키지가 포함되어 있습니다.
- org.springframework.security.oauth2.jwt
- org.springframework.security.oauth2.jose

## 6.9 OAuth 2.0 Resource Server — spring-security-oauth2-resource-server.jar
spring-security-oauth2-resource-server.jar에는 Spring Security의 OAuth 2.0 리소스 서버 지원이 포함되어 있습니다. OAuth 2.0 bearer 토큰을 통해 API를 보호하는 데 사용됩니다. 최상위 패키지는 org.springframework.security.oauth2.server.resource입니다.

## 6.10 ACL — spring-security-acl.jar
이 모듈에는 특수한 도메인 객체 ACL 구현이 포함되어 있습니다. 응용 프로그램 내의 특정 도메인 개체 인스턴스에 보안을 적용하는 데 사용됩니다. 최상위 패키지는 org.springframework.security.acls입니다.

## 6.11 CAS — spring-security-cas.jar
이 모듈에는 Spring Security의 CAS 클라이언트 통합이 포함되어 있습니다. CAS single sign-on 서버와 함께 Spring Security 웹 인증을 사용하려면 이를 사용해야합니다. 최상위 패키지는 org.springframework.security.cas입니다.

## 6.12 OpenID — spring-security-openid.jar
이 모듈에는 OpenID 웹 인증 지원이 포함되어 있습니다. 외부 OpenID 서버에 대해 사용자를 인증하는 데 사용됩니다. 최상위 패키지는 org.springframework.security.openid입니다. OpenID4Java가 필요합니다.

## 6.13 Test — spring-security-test.jar
이 모듈에는 Spring Security 테스트 지원이 포함되어 있습니다.

## 7. Samples
Spring Security에는 많은 샘플 애플리케이션이 포함되어 있습니다.



