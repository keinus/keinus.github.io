# Part II. Servlet Applications
여기서부턴 선택적으로 번역한다.

# 8. Hello Spring Security
## 8.1 Hello Spring Security (Boot)
### 8.1.3 Spring Boot Auto Configuration

**예시 코드**
```
package org.springframework.security.samples.config;

import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;

/**
 * @author Joe Grandja
 */
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

	// @formatter:off
	@Override
	protected void configure(HttpSecurity http) throws Exception {
		http
				.authorizeRequests(authorizeRequests ->
					authorizeRequests
						.antMatchers("/css/**", "/index").permitAll()
						.antMatchers("/user/**").hasRole("USER")
				)
				.formLogin(formLogin ->
					formLogin
						.loginPage("/login")
						.failureUrl("/login-error")
				);
	}
	// @formatter:on

	@Bean
	public UserDetailsService userDetailsService() {
		UserDetails userDetails = User.withDefaultPasswordEncoder()
				.username("user")
				.password("password")
				.roles("USER")
				.build();
		return new InMemoryUserDetailsManager(userDetails);
	}
}


package org.springframework.security.samples.web;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;

/**
 * @author Joe Grandja
 */
@Controller
public class MainController {

	@RequestMapping("/")
	public String root() {
		return "redirect:/index";
	}

	@RequestMapping("/index")
	public String index() {
		return "index";
	}

	@RequestMapping("/user/index")
	public String userIndex() {
		return "user/index";
	}

	@RequestMapping("/login")
	public String login() {
		return "login";
	}

	@RequestMapping("/login-error")
	public String loginError(Model model) {
		model.addAttribute("loginError", true);
		return "login";
	}

}
```

Springboot에서 자동으로 설정하는 것들.
- Spring Security의 기본 구성을 활성화하여 서블릿 필터를 springSecurityFilterChain이라는 Bean으로 작성합니다. 이 Bean은 응용 프로그램 내의 모든 보안(응용 프로그램 URL 보호, 제출 된 사용자 이름 및 암호 유효성 검증, 로그 형식으로 경로 재 지정 등)을 담당합니다. 
- 사용자 이름이 user이고 console에 기록되는 임의로 생성 된 password로 UserDetailsService Bean을 작성합니다. 
- 모든 요청에 대해 Servlet 컨테이너와 함께 springSecurityFilterChain Bean으로 필터를 등록합니다.

Spring Boot는 많은 정보를 자동으로 설정하지는 않습니다만, 하는일은 많습니다. 다음은 자동으로 구성하는 기능들입니다.
- 응용 프로그램과 상호 작용하기 위한 인증된 유저
- 디폴트 로그인 폼
- form-based 인증으로 인증하기 위해 사용자 이름이 user이고 콘솔에 적힌 비밀번호로 로그인할 수 있도록 구성 (앞의 예에서 비밀번호는 8e557245-73e2-4286-969a-ff57fe326336)
- BCrypt로 사용자 비밀번호 보호
- 사용자 로그아웃 기능
- CSRF 공격 방호
- 세션 고정 공격 방호
- Security Header 통합
 1. 안전한 요청을 위한 HTTP Strict Transport Security
 2. X-Content-Type-Options 통합
 3. Cache Control (static resource 캐싱을 허용하여 당신의 어플리케이션을 통해 오버라이드 가능.)
 4. X-XSS-Protection 통합
 5. X-Frame-Options 를 통합하여 Clickjacking 을 방지함
- 아래 Servlet API 함수를 통합:
 1. HttpServletRequest#getRemoteUser()
 2. HttpServletRequest.html#getUserPrincipal()
 3. HttpServletRequest.html#isUserInRole(java.lang.String)
 4. HttpServletRequest.html#login(java.lang.String, java.lang.String)
 5. HttpServletRequest.html#logout()




