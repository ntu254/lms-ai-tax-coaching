/**
 * Tự động Việt hóa toàn diện giao diện Đăng nhập & Đăng ký (Ai Coaching Vietnam)
 */
(function () {
	const DICT = {
		// Tiêu đề & phụ đề
		"Sign In": "Đăng nhập",
		"Welcome! Please sign in to continue.": "Chào mừng bạn trở lại. Hãy đăng nhập để tiếp tục.",
		"Let's setup your account.": "Tạo tài khoản để bắt đầu học tập.",
		"Continue": "Đăng nhập",
		"Create Account": "Đăng ký tài khoản",
		"Forgot password?": "Quên mật khẩu?",
		"Login with Email Link": "Đăng nhập bằng liên kết email",
		"Don't have an account?": "Chưa có tài khoản?",
		"Back to sign in": "Quay lại đăng nhập",
		"Send Link": "Gửi liên kết",
		"Please enter your email, we'll send you password reset link": "Nhập email để nhận liên kết đặt lại mật khẩu.",
		"Login": "Đăng nhập",
		"Log in": "Đăng nhập",
		"Login to your account": "Đăng nhập vào tài khoản",
		"Sign up": "Đăng ký tài khoản",
		"Sign Up": "Đăng ký tài khoản",
		"Forgot Password": "Quên mật khẩu",
		"Reset Password": "Đặt lại mật khẩu",
		"Enter your email address and we'll send you a link to reset your password": "Nhập địa chỉ email của bạn để nhận liên kết đặt lại mật khẩu.",

		// Nhãn & Placeholder
		"Email": "Địa chỉ email",
		"Email or Username": "Địa chỉ email hoặc Tên đăng nhập",
		"Password": "Mật khẩu",
		"Full Name": "Họ và tên",
		"User Category": "Đối tượng học viên",
		"Select a category": "Chọn đối tượng học viên",
		"Jane Doe": "Nguyễn Văn A",
		"jane@example.com": "email@example.com",

		// Nút bấm
		"Send Password Reset Link": "Gửi liên kết đặt lại mật khẩu",
		"Send OTP": "Gửi mã OTP",
		"Submit": "Xác nhận",
		"Back to Login": "Quay lại Đăng nhập",

		// Liên kết chuyển đổi
		"Forgot Password?": "Quên mật khẩu?",
		"Don't have an account? Sign up": "Chưa có tài khoản? Đăng ký ngay",
		"Have an account? Login": "Đã có tài khoản? Đăng nhập ngay",
		"Have an account? Log in": "Đã có tài khoản? Đăng nhập ngay",

		// Danh mục đối tượng
		"Business Owner": "Chủ doanh nghiệp / Giám đốc",
		"Manager (Sales/Marketing/Customer)": "Quản lý / Trưởng phòng",
		"Employee": "Nhân viên / Chuyên viên",
		"Student": "Sinh viên / Học viên",
		"Freelancer/Just looking": "Làm việc tự do / Tìm hiểu",
		"Others": "Khác",

		// Thông báo lỗi
		"Invalid login credentials": "Email hoặc mật khẩu không chính xác. Vui lòng kiểm tra lại.",
		"Invalid credentials, try again.": "Email hoặc mật khẩu không chính xác. Vui lòng thử lại.",
		"Email is required.": "Vui lòng nhập địa chỉ email hoặc tên đăng nhập.",
		"Password is required.": "Vui lòng nhập mật khẩu.",
		"Invalid Email.": "Vui lòng nhập địa chỉ email hợp lệ.",
		"Oops! Something went wrong.": "Đã xảy ra lỗi. Vui lòng thử lại.",
		"Something went wrong.": "Đã xảy ra lỗi. Vui lòng thử lại.",
		"Too many requests. Please try again later.": "Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau.",
		"Both login and password required": "Vui lòng nhập tên đăng nhập và mật khẩu.",
		"Please check your email.": "Vui lòng kiểm tra email của bạn.",
		"Password reset link has been sent to your email": "Liên kết đặt lại mật khẩu đã được gửi đến email của bạn.",
		"Reset link emailed": "Đã gửi liên kết đặt lại mật khẩu qua email",
		"Success": "Thành công",
		"Sent": "Đã gửi",
		"Send login link": "Gửi liên kết đăng nhập",
		"Login with password": "Đăng nhập bằng mật khẩu",
		"Didn't receive the link?": "Chưa nhận được liên kết?",
		"Resend": "Gửi lại",
		"Signup Disabled": "Đăng ký đã bị vô hiệu hóa",
		"Signups have been disabled for this website.": "Chức năng đăng ký trên trang web này đã bị vô hiệu hóa.",
		"Verification": "Xác minh",
		"Verification Code": "Mã xác minh",
		"Verify": "Xác minh",
		"Login token required": "Vui lòng nhập mã xác minh.",
		"Scan the QR Code and enter the resulting code displayed.": "Quét mã QR và nhập mã hiển thị trong ứng dụng xác thực.",
		"Can't scan the code?": "Không thể quét mã?",
		"Enter this setup key manually:": "Nhập khóa thiết lập này theo cách thủ công:",
		"Enter Code displayed in OTP App.": "Nhập mã hiển thị trong ứng dụng OTP.",
		"OTP setup using OTP App was not completed. Please contact Administrator.": "Chưa hoàn tất thiết lập ứng dụng OTP. Vui lòng liên hệ quản trị viên.",
		"SMS was not sent. Please contact Administrator.": "Không gửi được tin nhắn SMS. Vui lòng liên hệ quản trị viên.",
		"Verification code email not sent. Please contact Administrator.": "Không gửi được email chứa mã xác minh. Vui lòng liên hệ quản trị viên.",
		"Please enter a valid email.": "Vui lòng nhập địa chỉ email hợp lệ.",
		"Full name is required.": "Vui lòng nhập họ và tên.",
		"Please select a category.": "Vui lòng chọn đối tượng học viên.",
		"Please accept the terms to continue.": "Vui lòng đồng ý với điều khoản sử dụng.",
	};

	function localizeAuthPage() {
		if (!document.body.matches('[data-path="login"], .page-login, .auth-page')) {
			// Cũng kiểm tra nếu form login/signup hiện diện trên trang
			if (!document.querySelector('.form-signin, .signup-form, .login-content')) {
				return;
			}
		}

		// A shared navigation link keeps every authentication state connected to the LMS.
		const content = document.querySelector('body[data-path="login"] .page_content > div');
		if (content && !content.querySelector('.auth-brand-bar')) {
			const bar = document.createElement('nav');
			bar.className = 'auth-brand-bar';
			bar.setAttribute('aria-label', 'Điều hướng');
			bar.innerHTML = '<a class="auth-brand" href="/lms/" aria-label="Ai Coaching Vietnam - Trang chủ"><img src="/assets/lms/images/ai-coaching-vietnam.png" alt=""></a><a class="auth-home" href="/lms/">Về trang chủ</a>';
			content.prepend(bar);
		}
		// 1. Dịch các tiêu đề h4, h5, title
		document.querySelectorAll('.page-card-head h4, .page-card-head h3, .page-card-title').forEach(el => {
			const text = el.textContent.trim();
			if (DICT[text]) el.textContent = DICT[text];
		});

		// 2. Dịch phụ đề
		document.querySelectorAll('.page-card-subtitle, .page-card-head p').forEach(el => {
			const text = el.textContent.trim();
			if (DICT[text]) el.textContent = DICT[text];
		});

		// 3. Dịch các label
		document.querySelectorAll('label').forEach(label => {
			for (const [en, vi] of Object.entries(DICT)) {
				if (label.childNodes.length > 0) {
					label.childNodes.forEach(node => {
						if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() === en) {
							node.nodeValue = node.nodeValue.replace(en, vi);
						}
					});
				}
			}
		});

		// 4. Dịch các nút bấm (buttons)
		document.querySelectorAll('button.btn-login, button.btn-signup, button.btn-forgot, .page-card-actions button, .btn-login-option').forEach(btn => {
			const text = btn.textContent.trim();
			if (DICT[text]) {
				btn.textContent = DICT[text];
			}
		});

		// 5. Dịch các link điều hướng
		document.querySelectorAll('.sign-up-message a, a[href="#forgot"], a[href="#login"], a[href="#signup"]').forEach(a => {
			const text = a.textContent.trim();
			if (DICT[text]) {
				a.textContent = DICT[text];
			}
		});

		document.querySelectorAll('.sign-up-message').forEach(container => {
			container.childNodes.forEach(node => {
				if (node.nodeType === Node.TEXT_NODE && DICT[node.nodeValue.trim()]) {
					node.nodeValue = node.nodeValue.replace(node.nodeValue.trim(), DICT[node.nodeValue.trim()]);
				}
			});
		});
		// 6. Dịch placeholders
		document.querySelectorAll('input').forEach(input => {
			const ph = input.getAttribute('placeholder');
			if (ph && DICT[ph]) {
				input.setAttribute('placeholder', DICT[ph]);
			}
			if (input.id === 'login_email' && (!ph || ph === 'jane@example.com')) {
				input.setAttribute('placeholder', 'nhap-email@example.com');
			}
			if (input.id === 'login_password' && !ph) {
				input.setAttribute('placeholder', 'Nhập mật khẩu...');
			}
		});

		// 7. Dịch select options đối tượng
		document.querySelectorAll('#user_category option').forEach(opt => {
			const text = opt.textContent.trim();
			if (DICT[text]) {
				opt.textContent = DICT[text];
			}
		});

		// Translate known text nodes in the authentication forms, including messages
		// inserted asynchronously by Frappe. Preserve nested links and icons.
		document.querySelectorAll('.login-content, section.for-login, section.for-email-login, section.for-forgot, section.for-signup, section.for-login-with-email-link').forEach(container => {
			const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
			let node;
			while ((node = walker.nextNode())) {
				if (node.parentElement?.closest('script, style, textarea')) continue;
				const text = node.nodeValue.trim();
				if (DICT[text]) node.nodeValue = node.nodeValue.replace(text, DICT[text]);
			}
		});

		// 8. Dịch banner thông báo nếu có
		document.querySelectorAll('.es-alert__title, .field-error').forEach(err => {
			const text = err.textContent.trim();
			if (DICT[text]) {
				err.textContent = DICT[text];
			}
		});
	}

	let isLocalizing = false;
	let timeoutId = null;

	function safeLocalize() {
		if (isLocalizing) return;
		isLocalizing = true;
		try {
			localizeAuthPage();
		} finally {
			setTimeout(() => {
				isLocalizing = false;
			}, 30);
		}
	}

	// Chạy ngay khi DOM sẵn sàng
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', safeLocalize);
	} else {
		safeLocalize();
	}

	// Frappe uses #login as its default route. Remove the redundant fragment
	// after its router has selected the login form, keeping any return URL query.
	function cleanLoginFragment() {
		if (window.location.hash === '#login') {
			window.history.replaceState(window.history.state, '', window.location.pathname + window.location.search);
		}
	}
	window.addEventListener('load', () => setTimeout(cleanLoginFragment, 0));
	window.addEventListener('hashchange', () => setTimeout(cleanLoginFragment, 0));
	// Lắng nghe thay đổi tab (#login, #signup, #forgot)
	window.addEventListener('hashchange', () => {
		setTimeout(safeLocalize, 50);
		setTimeout(safeLocalize, 200);
	});

	// Quan sát DOM mutations có debounce để bắt kịp khi Frappe re-render
	const observer = new MutationObserver(() => {
		if (timeoutId) clearTimeout(timeoutId);
		timeoutId = setTimeout(safeLocalize, 60);
	});

	observer.observe(document.documentElement, {
		childList: true,
		subtree: true,
	});
})();
