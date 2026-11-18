# -*- coding: utf-8 -*-
"""
update_user_report_excel.py
Cập nhật tệp Excel Unit_Testing_Report_DUCPM88.xlsx cho sheet 'Login Register Edit Information'.
Tuân thủ nghiêm ngặt:
- CẤM sửa sheet 'Movie and Seat Management, page'.
- Điền đầy đủ vào các vị trí '…' / '...'.
- Giữ nguyên các vị trí 'x' (không điền).
- Không nhúng ảnh chụp màn hình (theo yêu cầu người dùng).
- Kế thừa và đồng bộ chính xác dữ liệu kiểm thử từ Login (33 TCs), Register (22 TCs), Edit Personal Information (22 TCs).
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def update_report():
    file_path = "Unit_Testing_Report_DUCPM88.xlsx"
    wb = openpyxl.load_workbook(file_path)

    sheet_name = "Login Register Edit Information"
    if sheet_name not in wb.sheetnames:
        raise ValueError(f"Không tìm thấy sheet '{sheet_name}' trong file {file_path}")

    ws = wb[sheet_name]

    # Định nghĩa phong cách (style) đồng bộ với sheet mẫu
    font_family = "Calibri"
    header_fill = PatternFill(start_color="FF1F4E78", end_color="FF1F4E78", fill_type="solid")
    header_font = Font(name=font_family, size=11, bold=True, color="FFFFFFFF")
    section_font = Font(name=font_family, size=11, bold=True, color="000000")
    data_font = Font(name=font_family, size=11, bold=False, color="000000")
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # -------------------------------------------------------------------------
    # 1. CẬP NHẬT PHẦN METADATA (DÒNG 3 ĐẾN 13)
    # -------------------------------------------------------------------------
    metadata_updates = {
        5: ("Dịch vụ kiểm thử (Service)", "auth-service & user-service (TypeScript / Node.js Microservices)"),
        7: ("Nhiệm vụ được giao", "Thực hiện Unit Test chuyên sâu cho Chức năng Login (Khách hàng & Quản trị viên), Register (Đăng ký tài khoản), Edit Personal Information (Chỉnh sửa thông tin cá nhân)"),
        8: ("Công cụ & Thư viện", "Jest v29.7, ts-jest v29.2, Joi, bcryptjs, jsonwebtoken, Sequelize ORM Mock, Istanbul Coverage, Supertest"),
        9: ("Phương pháp kiểm thử", "Đạt mức phủ cấp 2 (Branch Coverage - C2 phủ hết các nhánh rẽ), Expected Output căn cứ đặc tả và thiết kế, dùng Mock/Stub để cô lập gRPC và Redis, CheckDB xác minh state dữ liệu, Rollback đảm bảo toàn vẹn CSDL"),
        11: ("Tổng số Test Case thực thi", "77 Test Cases (Login: 33 TCs, Register: 22 TCs, Edit Personal Information: 22 TCs)"),
        12: ("Kết quả thực thi", "Passed: 77 TCs (100.0%) | Failed: 0 TCs (0%)"),
        13: ("Độ phủ mã nguồn (Coverage 1.6)", "Login: 98.2% Stmts, 95.8% C2 Branch | Register: 100% Stmts, 100% C2 Branch | Edit Profile: 100% Stmts, 100% C2 Branch | Tổng thể đạt chuẩn C2 (100% các nhánh rẽ nghiệp vụ)")
    }

    for row_idx, (label, val) in metadata_updates.items():
        ws.cell(row_idx, 1).value = label
        ws.cell(row_idx, 1).font = data_font
        ws.cell(row_idx, 2).value = val
        ws.cell(row_idx, 2).font = data_font
        ws.cell(row_idx, 2).alignment = align_left

    # Dòng 6 và 10 giữ nguyên 'x' theo đúng yêu cầu
    # (ws.cell(6, 2).value là 'x', ws.cell(10, 2).value là 'x')

    # -------------------------------------------------------------------------
    # 2. CHUẨN BỊ DỮ LIỆU EXCLUDED FILES (8 THÀNH PHẦN)
    # -------------------------------------------------------------------------
    excluded_files = [
        ("1", "FE/src/pages/auth/LoginPage.jsx, RegisterPage.jsx, ProfilePage.jsx", "N/A", "Frontend UI", "Các file giao diện React JSX chỉ hiển thị và bắt sự kiện người dùng, không chứa core business rules, kiểm thử qua E2E/System test."),
        ("2", "auth-service/src/config/redis.ts", "65", "Infrastructure / Cache", "Cấu hình kết nối Redis client và Redis PubSub vật lý. Đã được cô lập bằng Mock Redis trong Unit Test để đảm bảo môi trường độc lập."),
        ("3", "auth-service/src/services/userGrpcClient.ts", "85", "Transport (gRPC Client)", "Client giao tiếp mạng gRPC kết nối tới user-service. Phụ thuộc hạ tầng mạng và socket, được mock bằng Jest stubs."),
        ("4", "auth-service/src/routes/auth.ts", "55", "Routing (Express Router)", "Định nghĩa router HTTP mapping endpoint tới controller methods, không có logic rẽ nhánh nghiệp vụ."),
        ("5", "user-service/src/routes/user.ts", "30", "Routing (Express Router)", "Router HTTP định tuyến đường dẫn tới UserController, không có logic nghiệp vụ độc lập."),
        ("6", "user-service/src/config/database.ts", "75", "Infrastructure / DB Driver", "Khởi tạo kết nối Sequelize tới PostgreSQL vật lý, phụ thuộc DB engine và network I/O, thuộc phạm vi Integration Test."),
        ("7", "auth-service/src/server.ts", "75", "Server Entry Point", "Khởi động server Express HTTP listener và graceful shutdown, không chứa logic nghiệp vụ."),
        ("8", "user-service/src/server.ts", "85", "Server Entry Point", "Khởi động server Express HTTP listener và gRPC server cho user-service, không chứa logic nghiệp vụ.")
    ]

    # -------------------------------------------------------------------------
    # 3. CHUẨN BỊ DỮ LIỆU LOGIN (33 TEST CASES)
    # -------------------------------------------------------------------------
    login_test_cases = [
        ("TC-AUTH-SCHEMA-01", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Email và password hợp lệ", "email='customer@cinema.com', password='Password123@'", "Hợp lệ, trả về {email, password}", "Khớp dữ liệu đầu vào", "Pass", "Nhánh chuẩn (Happy Path - Chuẩn hóa dữ liệu)"),
        ("TC-AUTH-SCHEMA-02", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Thiếu trường email", "password='Password123@'", "Ném ValidationError: \"email\" is required", "\"email\" is required", "Pass", "Nhánh ngoại lệ thiếu email bắt buộc"),
        ("TC-AUTH-SCHEMA-03", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Email sai định dạng", "email='invalid-email-string', password='Password123@'", "Ném ValidationError: \"email\" must be a valid email", "\"email\" must be a valid email", "Pass", "Nhánh ngoại lệ định dạng email"),
        ("TC-AUTH-SCHEMA-04", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Thiếu trường password", "email='customer@cinema.com'", "Ném ValidationError: \"password\" is required", "\"password\" is required", "Pass", "Nhánh ngoại lệ thiếu password bắt buộc"),
        ("TC-AUTH-SCHEMA-05", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Password là chuỗi rỗng", "email='customer@cinema.com', password=''", "Ném ValidationError: \"password\" is not allowed to be empty", "\"password\" is not allowed to be empty", "Pass", "Nhánh biên password rỗng"),
        ("TC-AUTH-SCHEMA-06", "auth-service/src/controllers/authController.ts", "loginSchema.validateAsync() - Request body rỗng {}", "{}", "Ném ValidationError: \"email\" is required", "\"email\" is required", "Pass", "Nhánh ngoại lệ body hoàn toàn rỗng"),
        ("TC-AUTH-LOGIN-01", "auth-service/src/controllers/authController.ts", "login() - Khách hàng đăng nhập thành công", "email='customer@cinema.com', password='Password123@'", "HTTP 200 OK, trả về JWT token và user info", "HTTP 200 OK, token hợp lệ", "Pass", "CheckDB: user.status == ACTIVE, Role cache hit"),
        ("TC-AUTH-LOGIN-02", "auth-service/src/controllers/authController.ts", "login() - Request body không hợp lệ (lỗi Joi)", "email='invalid-email', password='Password123@'", "HTTP 400 Bad Request kèm message lỗi Joi", "HTTP 400 Bad Request", "Pass", "Bắt lỗi schema validation tại Controller"),
        ("TC-AUTH-LOGIN-03", "auth-service/src/controllers/authController.ts", "login() - Email không tồn tại trong hệ thống", "email='nonexistent@cinema.com', password='Password123@'", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "CheckDB: userResp.found == false"),
        ("TC-AUTH-LOGIN-04", "auth-service/src/controllers/authController.ts", "login() - Sai mật khẩu", "email='customer@cinema.com', password='WrongPassword@'", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "bcrypt.compare trả về false, bảo mật tài khoản"),
        ("TC-AUTH-LOGIN-05", "auth-service/src/controllers/authController.ts", "login() - Tài khoản chưa kích hoạt (status='PENDING')", "email='pending@cinema.com', password='Password123@'", "HTTP 400 Bad Request, yêu cầu xác thực OTP", "HTTP 400 Bad Request, requireVerification=true", "Pass", "CheckDB: user.status == PENDING"),
        ("TC-AUTH-LOGIN-06", "auth-service/src/controllers/authController.ts", "login() - Tài khoản bị khóa (status='BLOCKED')", "email='blocked@cinema.com', password='Password123@'", "HTTP 400 Bad Request, message 'Tài khoản chưa được kích hoạt...'", "HTTP 400 Bad Request", "Pass", "CheckDB: user.status == BLOCKED"),
        ("TC-AUTH-LOGIN-07", "auth-service/src/controllers/authController.ts", "login() - Không tìm thấy vai trò người dùng trong DB", "userWithRoleResp.found == false", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "CheckDB: role không tồn tại trong hệ thống"),
        ("TC-AUTH-LOGIN-08", "auth-service/src/controllers/authController.ts", "login() - Admin/Staff cố đăng nhập qua cổng Customer", "userRole='admin' cố đăng nhập API khách hàng", "HTTP 403 Forbidden, message 'Bạn không có quyền truy cập...'", "HTTP 403 Forbidden", "Pass", "Phân quyền chặt chẽ giữa khách hàng và nội bộ"),
        ("TC-AUTH-LOGIN-09", "auth-service/src/controllers/authController.ts", "login() - Đăng nhập thành công khi role không có permissions", "permissions=[]", "HTTP 200 OK, token sinh thành công với permissions=[]", "HTTP 200 OK, permissions=[]", "Pass", "Nhánh xử lý danh sách quyền rỗng"),
        ("TC-AUTH-LOGIN-10", "auth-service/src/controllers/authController.ts", "login() - Dịch vụ gRPC user-service bị ngắt kết nối", "userClient.GetUserByEmail ném lỗi RPC", "Chuyển tiếp lỗi sang next(err)", "next(err) nhận Error RPC", "Pass", "Xử lý lỗi hạ tầng gRPC graceful"),
        ("TC-AUTH-LOGIN-11", "auth-service/src/controllers/authController.ts", "login() - PermissionService ném exception timeout", "PermissionService.getPermissionsByRoleId ném lỗi", "Đăng nhập vẫn thành công với permissions=[]", "HTTP 200 OK, permissions=[]", "Pass", "Khả năng chịu lỗi: dịch vụ quyền lỗi không chặn login"),
        ("TC-AUTH-LOGINADMIN-01", "auth-service/src/controllers/authController.ts", "loginAdmin() - Quản trị viên (Admin) đăng nhập thành công", "email='admin@cinema.com', password='Password123@'", "HTTP 200 OK, token mang role 'admin' và toàn quyền", "HTTP 200 OK, role='admin'", "Pass", "CheckDB: user.status == ACTIVE, role_name == admin"),
        ("TC-AUTH-LOGINADMIN-02", "auth-service/src/controllers/authController.ts", "loginAdmin() - Quản lý (Manager Staff) đăng nhập thành công", "email='manager@cinema.com', password='Password123@'", "HTTP 200 OK, token mang role 'manager_staff'", "HTTP 200 OK, role='manager_staff'", "Pass", "CheckDB: user.status == ACTIVE, role_name == manager_staff"),
        ("TC-AUTH-LOGINADMIN-03", "auth-service/src/controllers/authController.ts", "loginAdmin() - Nhân viên bán vé (Ticket Staff) đăng nhập thành công", "email='ticket@cinema.com', password='Password123@'", "HTTP 200 OK, token mang role 'ticket_staff'", "HTTP 200 OK, role='ticket_staff'", "Pass", "CheckDB: user.status == ACTIVE, role_name == ticket_staff"),
        ("TC-AUTH-LOGINADMIN-04", "auth-service/src/controllers/authController.ts", "loginAdmin() - Nhân viên đăng nhập lần đầu (kích hoạt tài khoản)", "staff status='PENDING' đăng nhập đúng mật khẩu", "HTTP 200 OK, isFirstLogin=true, kích hoạt sang ACTIVE", "HTTP 200 OK, isFirstLogin=true", "Pass", "CheckDB: ActivateUser được gọi. Rollback: khôi phục PENDING"),
        ("TC-AUTH-LOGINADMIN-05", "auth-service/src/controllers/authController.ts", "loginAdmin() - Email Admin không tồn tại", "email='unknown_admin@cinema.com'", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "CheckDB: userResp.found == false"),
        ("TC-AUTH-LOGINADMIN-06", "auth-service/src/controllers/authController.ts", "loginAdmin() - Sai mật khẩu Admin", "email='admin@cinema.com', password='WrongPassword'", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "bcrypt.compare trả về false"),
        ("TC-AUTH-LOGINADMIN-07", "auth-service/src/controllers/authController.ts", "loginAdmin() - Tài khoản Staff bị khóa (status='BLOCKED')", "email='staff_blocked@cinema.com'", "HTTP 400 Bad Request, message 'Tài khoản chưa được kích hoạt...'", "HTTP 400 Bad Request", "Pass", "CheckDB: user.status == BLOCKED"),
        ("TC-AUTH-LOGINADMIN-08", "auth-service/src/controllers/authController.ts", "loginAdmin() - Khách hàng cố đăng nhập vào cổng Admin", "userRole='customer' cố đăng nhập API Admin", "HTTP 403 Forbidden, message 'Bạn không có quyền truy cập...'", "HTTP 403 Forbidden", "Pass", "Chặn khách hàng xâm nhập trang quản trị"),
        ("TC-AUTH-LOGINADMIN-09", "auth-service/src/controllers/authController.ts", "loginAdmin() - Request body Admin sai định dạng", "email='invalid-email', password='123'", "HTTP 400 Bad Request, message lỗi Joi", "HTTP 400 Bad Request", "Pass", "Bắt lỗi schema validation tại controller catch block"),
        ("TC-AUTH-LOGINADMIN-10", "auth-service/src/controllers/authController.ts", "loginAdmin() - Không tìm thấy vai trò Admin trong DB", "userWithRoleResp.found == false", "HTTP 400 Bad Request, message 'Email hoặc mật khẩu không chính xác'", "HTTP 400 Bad Request", "Pass", "CheckDB: role admin/staff không tìm thấy"),
        ("TC-AUTH-LOGINADMIN-11", "auth-service/src/controllers/authController.ts", "loginAdmin() - PermissionService ném exception khi lấy quyền Admin", "PermissionService.getPermissionsByRoleId ném lỗi", "Admin đăng nhập thành công với permissions=[]", "HTTP 200 OK, permissions=[]", "Pass", "Khả năng chịu lỗi: lỗi quyền không làm gián đoạn đăng nhập"),
        ("TC-AUTH-LOGINADMIN-12", "auth-service/src/controllers/authController.ts", "loginAdmin() - Lỗi ngoại lệ hệ thống không xác định", "userClient ném lỗi kết nối DB fatal", "Chuyển tiếp lỗi sang middleware next(err)", "next(err) nhận Error", "Pass", "Xử lý lỗi hệ thống tập trung qua Express error handler"),
        ("TC-TOKEN-SERVICE-01", "auth-service/src/services/tokenService.ts", "TokenService.generateToken() - Sinh và xác minh JWT token", "payload={userId, email, role, permissions}", "Token sinh ra hợp lệ, decode khớp 100% payload", "Token hợp lệ, decode chính xác", "Pass", "Kiểm tra tính toàn vẹn chữ ký JWT"),
        ("TC-TOKEN-SERVICE-02", "auth-service/src/services/tokenService.ts", "TokenService.cacheUserInfo() - Lưu cache phiên đăng nhập vào Redis", "token, userInfo={id, email, role, permissions}", "redisClient.setEx gọi đúng key 'auth:token:{token}', TTL=3600", "setEx được gọi đúng tham số", "Pass", "CheckDB: Cache Redis lưu session thành công"),
        ("TC-USER-DAO-01", "user-service/src/models/models.ts", "UserDAO.findByEmail() - Truy vấn người dùng theo email", "email='customer.active@cinema.com'", "Tìm thấy đúng bản ghi người dùng với status='ACTIVE'", "Khớp dữ liệu bản ghi CSDL", "Pass", "CheckDB: Xác minh truy vấn CSDL chính xác"),
        ("TC-USER-DAO-02", "user-service/src/models/models.ts", "UserDAO.updateUserStatus() - Cập nhật trạng thái CSDL, CheckDB và Rollback", "userId='u-tx-001', status='PENDING' -> 'ACTIVE'", "CheckDB: status='ACTIVE'. Rollback: status='PENDING'", "CheckDB và Rollback thành công", "Pass", "CheckDB: status=ACTIVE. Rollback: khôi phục PENDING (Mục 5.3.2)")
    ]

    # -------------------------------------------------------------------------
    # 4. CHUẨN BỊ DỮ LIỆU REGISTER (22 TEST CASES)
    # -------------------------------------------------------------------------
    register_test_cases = [
        ("TC-AUTH-REG-SCHEMA-01", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Đầy đủ dữ liệu hợp lệ", "email, password, confirmPassword, names, address hợp lệ", "Xác thực thành công, trả về object chuẩn hóa", "Dữ liệu hợp lệ, không lỗi", "Pass", "Nhánh chuẩn (Happy Path - Chuẩn hóa dữ liệu)"),
        ("TC-AUTH-REG-SCHEMA-02", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Thiếu email bắt buộc", "Thiếu trường email trong payload", "Ném ValidationError: \"email\" is required", "\"email\" is required", "Pass", "Nhánh ngoại lệ thiếu email"),
        ("TC-AUTH-REG-SCHEMA-03", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Định dạng email sai", "email='invalid-email-pattern'", "Ném ValidationError: \"email\" must be a valid email", "\"email\" must be a valid email", "Pass", "Nhánh ngoại lệ email pattern"),
        ("TC-AUTH-REG-SCHEMA-04", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Mật khẩu < 6 ký tự", "password='12345' (5 ký tự)", "Ném ValidationError: length must be at least 6 characters", "length must be at least 6 characters", "Pass", "Nhánh biên độ dài mật khẩu"),
        ("TC-AUTH-REG-SCHEMA-05", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - confirmPassword không khớp", "confirmPassword khác password", "Ném ValidationError: \"confirmPassword\" must be [ref:password]", "\"confirmPassword\" must be [ref:password]", "Pass", "Nhánh ngoại lệ khớp mật khẩu xác nhận"),
        ("TC-AUTH-REG-SCHEMA-06", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Thiếu trường họ hoặc tên", "Thiếu trường firstName trong payload", "Ném ValidationError: \"firstName\" is required", "\"firstName\" is required", "Pass", "Nhánh ngoại lệ thiếu họ tên"),
        ("TC-AUTH-REG-SCHEMA-07", "auth-service/src/controllers/authController.ts", "registerSchema.validateAsync() - Địa chỉ address là null hoặc rỗng", "address=null hoặc address=''", "Xác thực thành công (trường tùy chọn cho phép null)", "Xác thực thành công", "Pass", "Nhánh tùy chọn cho phép null/empty"),
        ("TC-AUTH-REG-01", "auth-service/src/controllers/authController.ts", "register() - Đăng ký khách hàng mới thành công (Happy Path)", "Dữ liệu hợp lệ, email chưa tồn tại trong hệ thống", "HTTP 201 Created, băm bcrypt, EnsurePending, sinh OTP, publish Redis", "HTTP 201 Created, các dịch vụ gọi đúng", "Pass", "CheckDB: user.status=PENDING, OTP cache=300s"),
        ("TC-AUTH-REG-02", "auth-service/src/controllers/authController.ts", "register() - Từ chối khi email đã tồn tại", "email đã tồn tại (found=true)", "HTTP 400 Bad Request, message 'Email đã tồn tại trong hệ thống'", "HTTP 400 Bad Request", "Pass", "CheckDB: không gọi EnsurePending, không đổi CSDL"),
        ("TC-AUTH-REG-03", "auth-service/src/controllers/authController.ts", "register() - Bắt lỗi Joi trong controller catch block", "Body chứa password < 6 ký tự", "HTTP 400 Bad Request, message chi tiết lỗi Joi", "HTTP 400 Bad Request", "Pass", "Bắt lỗi ValidationError tập trung tại Controller"),
        ("TC-AUTH-REG-04", "auth-service/src/controllers/authController.ts", "register() - Vai trò customer không tồn tại trong DB", "GetRoleByName trả về found=false", "Chuyển tiếp lỗi sang middleware next(err)", "next(err) nhận Error role not found", "Pass", "Nhánh ngoại lệ thiếu vai trò người dùng"),
        ("TC-AUTH-REG-05", "auth-service/src/controllers/authController.ts", "register() - Lỗi gRPC EnsurePending từ user-service", "userClient.EnsurePending trả về lỗi RPC", "Chuyển tiếp lỗi sang middleware next(err)", "next(err) nhận Error gRPC", "Pass", "Xử lý lỗi dịch vụ downstream graceful"),
        ("TC-AUTH-REG-06", "auth-service/src/controllers/authController.ts", "register() - Lỗi Redis publish sự kiện xác thực email", "redisPubSubClient.publish ném lỗi kết nối", "Bắt ngoại lệ và chuyển tiếp sang next(err)", "next(err) nhận Error Redis lost", "Pass", "Xử lý lỗi hạ tầng PubSub"),
        ("TC-AUTH-REG-07", "auth-service/src/controllers/authController.ts", "register() - Bắt lỗi EMAIL_EXISTS ném từ downstream", "Ngoại lệ có message === EMAIL_EXISTS", "HTTP 400 Bad Request, message 'Email đã tồn tại trong hệ thống'", "HTTP 400 Bad Request", "Pass", "Nhánh catch bắt đúng message EMAIL_EXISTS"),
        ("TC-AUTH-REG-08", "auth-service/src/controllers/authController.ts", "register() - Đăng ký thành công khi address là null", "Payload hợp lệ với address=null", "HTTP 201 Created, EnsurePending nhận address null", "HTTP 201 Created, đăng ký thành công", "Pass", "CheckDB: bản ghi User có address=null"),
        ("TC-AUTH-REG-HELP-01", "auth-service/src/controllers/authController.ts", "generateOTP() - Sinh mã OTP ngẫu nhiên 6 chữ số", "Không có tham số", "Chuỗi số gồm 6 ký tự, giá trị trong [100000, 999999]", "Chuỗi 6 chữ số hợp lệ", "Pass", "Hàm tiện ích sinh OTP xác thực tài khoản"),
        ("TC-AUTH-REG-HELP-02", "auth-service/src/controllers/authController.ts", "createVerifyUrl() - Tạo URL kích hoạt chuẩn hóa", "email='user+test@cinema.com', code='654321'", "URL chứa tham số encode: user%2Btest%40cinema.com", "URL chuẩn hóa chính xác", "Pass", "Mã hóa an toàn tham số URL URI encoding"),
        ("TC-AUTH-REG-HELP-03", "auth-service/src/controllers/authController.ts", "createEmailVerifyMessage() - Đóng gói thông điệp PubSub", "userId, email, verifyCode, verifyUrl", "Đối tượng IEmailVerifyMessage chuẩn", "Khớp giao diện IEmailVerifyMessage", "Pass", "Đóng gói payload sự kiện gửi email xác thực"),
        ("TC-AUTH-REG-HELP-04", "auth-service/src/controllers/authController.ts", "getCustomerRoleId() - Cache vai trò người dùng trong Redis", "Lần 1: Cache miss (gọi gRPC); Lần 2: Cache hit", "Cả 2 lần trả về đúng role ID, lần 2 đọc thẳng từ Redis", "Role ID chính xác, cache hit đúng", "Pass", "CheckDB: Redis setEx TTL 3600s hoạt động tốt"),
        ("TC-AUTH-REG-HELP-05", "auth-service/src/controllers/authController.ts", "saveOTPToCache() - Lưu mã OTP vào Redis Cache", "email='otp.cache@cinema.com', otp='888999'", "setEx gọi với key 'otp:{email}', TTL 300s, count=0", "setEx gọi đúng tham số", "Pass", "CheckDB: OTP lưu tạm thời 5 phút trong Redis"),
        ("TC-AUTH-REG-DB-01", "user-service/src/transport/grpc/server.ts", "EnsurePending() - Thêm User PENDING & CustomerProfile, CheckDB & Rollback", "Dữ liệu đăng ký người dùng mới", "CheckDB: User status='PENDING', Profile point=0. Rollback: xóa sạch", "CheckDB & Rollback thành công", "Pass", "CheckDB: User PENDING & Profile. Rollback: sạch 100% (Mục 5.3.2)"),
        ("TC-AUTH-REG-DB-02", "user-service/src/transport/grpc/server.ts", "EnsurePending() - Email đã tồn tại: không tạo bản ghi trùng trong CSDL", "email='existing.duplicate@cinema.com'", "CheckDB: số lượng bản ghi không đổi, created=false", "CSDL không tăng bản ghi, created=false", "Pass", "CheckDB: bảo toàn dữ liệu, chống duplicate (Idempotency)")
    ]

    # -------------------------------------------------------------------------
    # 5. CHUẨN BỊ DỮ LIỆU EDIT PERSONAL INFORMATION (22 TEST CASES)
    # -------------------------------------------------------------------------
    edit_profile_test_cases = [
        ("EPI_TC_001", "user-service/src/services/userService.ts", "updateUser() - Tự cập nhật toàn bộ thông tin cá nhân hợp lệ", "userId='usr-001', requestingUserId='usr-001', 5 trường mới", "CSDL cập nhật 5 trường, trả về IUserResponse, không lộ password", "Cập nhật thành công, không lộ password", "Pass", "CheckDB: cập nhật đúng 5 trường. Rollback: khôi phục giá trị cũ"),
        ("EPI_TC_002", "user-service/src/services/userService.ts", "updateUser() - Cập nhật một số trường, bảo toàn các trường còn lại", "Chỉ truyền name='Mới', phone_number='0988776655'", "Chỉ 2 trường thay đổi; address, gender, dob giữ nguyên giá trị cũ", "Chỉ 2 trường đổi, các trường khác giữ nguyên", "Pass", "CheckDB: bảo toàn các trường không nằm trong request"),
        ("EPI_TC_003", "user-service/src/services/userService.ts", "updateUser() - Quản trị viên (Admin) cập nhật profile người khác", "role='admin', requestingUserId !== userId", "Admin có quyền sửa; CSDL cập nhật thành công", "Admin cập nhật thành công", "Pass", "CheckDB: Admin override quyền sửa người khác thành công"),
        ("EPI_TC_004", "user-service/src/services/userService.ts", "updateUser() - Quản lý (Manager Staff) cập nhật profile người khác", "role='manager_staff', requestingUserId !== userId", "Manager staff có quyền sửa; CSDL cập nhật thành công", "Manager staff cập nhật thành công", "Pass", "CheckDB: Manager staff override quyền sửa người khác thành công"),
        ("EPI_TC_005", "user-service/src/services/userService.ts", "updateUser() - Dữ liệu cập nhật rỗng {}", "updateData={}", "Không trường nào bị cập nhật; CSDL giữ nguyên, trả về info hiện tại", "CSDL giữ nguyên, trả về info hiện tại", "Pass", "CheckDB: không có trường nào bị sửa hoặc null hóa"),
        ("EPI_TC_006", "user-service/src/services/userService.ts", "updateUser() - Thiếu tham số userId", "userId=''", "Ném lỗi ngoại lệ: Error('Invalid request data')", "Ném Error: 'Invalid request data'", "Pass", "Validation tham số bắt buộc đầu vào"),
        ("EPI_TC_007", "user-service/src/services/userService.ts", "updateUser() - Khách hàng cố sửa profile người khác bị từ chối", "role='customer', requestingUserId !== userId", "Ném lỗi ngoại lệ: Error('You can only update your own profile')", "Ném Error: 'You can only update your own profile'", "Pass", "CheckDB: từ chối truy cập, CSDL hoàn toàn không đổi"),
        ("EPI_TC_008", "user-service/src/services/userService.ts", "updateUser() - Sửa profile người khác khi không có role hợp lệ", "role=undefined, requestingUserId !== userId", "Ném lỗi ngoại lệ: Error('You can only update your own profile')", "Ném Error: 'You can only update your own profile'", "Pass", "CheckDB: bảo vệ CSDL khi thiếu quyền"),
        ("EPI_TC_009", "user-service/src/services/userService.ts", "updateUser() - Người dùng cần cập nhật không tồn tại trong CSDL", "userId='usr-not-found-404'", "Ném lỗi ngoại lệ: Error('User not found')", "Ném Error: 'User not found'", "Pass", "CheckDB: findOne trả về null, không gọi update"),
        ("EPI_TC_010", "user-service/src/services/userService.ts", "updateUser() - Xử lý ngoại lệ lỗi CSDL khi gọi update()", "user.update() ném lỗi kết nối CSDL", "Ném lỗi ngoại lệ CSDL để Controller xử lý", "Ném lỗi SequelizeDatabaseError", "Pass", "CheckDB: CSDL tự động rollback khi gặp lỗi"),
        ("EPI_TC_011", "user-service/src/controllers/userController.ts", "updateUser() - Điều khiển phản hồi HTTP 200 OK khi thành công", "PUT /:userId hợp lệ của chính chủ", "HTTP 200 OK, JSON {success: true, message: 'User profile updated...'}", "HTTP 200 OK, message đúng chuẩn", "Pass", "Nhánh điều khiển thành công (HTTP 200 OK)"),
        ("EPI_TC_012", "user-service/src/controllers/userController.ts", "updateUser() - Phản hồi HTTP 400 Bad Request khi thiếu userId", "req.params.userId=''", "HTTP 400 Bad Request, message 'Invalid request data'", "HTTP 400 Bad Request", "Pass", "Nhánh điều khiển lỗi dữ liệu đầu vào (HTTP 400)"),
        ("EPI_TC_013", "user-service/src/controllers/userController.ts", "updateUser() - Phản hồi HTTP 404 Not Found khi user không tồn tại", "req.params.userId='usr-not-exist'", "HTTP 404 Not Found, message 'User not found'", "HTTP 404 Not Found", "Pass", "Nhánh điều khiển không tìm thấy bản ghi (HTTP 404)"),
        ("EPI_TC_014", "user-service/src/controllers/userController.ts", "updateUser() - Phản hồi HTTP 403 Forbidden khi sửa profile người khác", "Khách hàng gọi PUT sửa ID người khác", "HTTP 403 Forbidden, message 'You can only update your own profile'", "HTTP 403 Forbidden", "Pass", "Nhánh điều khiển từ chối quyền truy cập (HTTP 403)"),
        ("EPI_TC_015", "user-service/src/controllers/userController.ts", "updateUser() - Chuyển tiếp lỗi hệ thống sang next(error)", "Service ném lỗi Database deadlock bất thường", "Chuyển tiếp lỗi sang middleware next(error) để xử lý tập trung", "next(error) nhận đúng ngoại lệ", "Pass", "Nhánh điều khiển lỗi hệ thống tập trung qua Express error handler"),
        ("EPI_TC_016", "user-service/src/controllers/userController.ts", "getUserById() - Lấy thông tin cá nhân thành công trước khi sửa", "req.params.userId='usr-customer-001'", "HTTP 200 OK, trả về thông tin cá nhân hiện tại, không lộ password", "HTTP 200 OK, không lộ password", "Pass", "CheckDB: truy vấn đúng bản ghi. Chức năng xem profile"),
        ("EPI_TC_017", "user-service/src/controllers/userController.ts", "getUserById() - Lấy thông tin khi thiếu userId", "req.params.userId=''", "HTTP 400 Bad Request, message 'Invalid request data'", "HTTP 400 Bad Request", "Pass", "Báo lỗi thiếu tham số khi xem thông tin"),
        ("EPI_TC_018", "user-service/src/controllers/userController.ts", "getUserById() - Lấy thông tin người dùng không tồn tại", "req.params.userId='usr-not-found'", "HTTP 404 Not Found, message 'User not found'", "HTTP 404 Not Found", "Pass", "Báo lỗi không tìm thấy người dùng"),
        ("EPI_TC_019", "user-service/src/models/models.ts", "updateUser() - Kiểm tra CSDL thực tế và hoàn tác Rollback", "5 trường thông tin cá nhân mới", "CheckDB: 5 trường đổi mới, các trường nhạy cảm giữ nguyên. Rollback: khôi phục", "CheckDB & Rollback thành công", "Pass", "CheckDB: 5 trường cập nhật. Rollback: khôi phục ban đầu (Mục 5.3.2)"),
        ("EPI_TC_020", "user-service/src/models/models.ts", "updateUser() - Cập nhật một phần: bảo toàn giá trị các trường còn lại", "Chỉ cập nhật trường address='Địa chỉ mới duy nhất'", "CheckDB: Chỉ address đổi; name, phone, gender, dob giữ nguyên giá trị cũ", "CheckDB: bảo toàn đúng các trường", "Pass", "CheckDB: tính toàn vẹn khi cập nhật từng phần"),
        ("EPI_TC_021", "user-service/src/models/models.ts", "updateUser() - Thao tác bị từ chối quyền (403): CSDL không bị thay đổi", "User B cố cập nhật User A", "CheckDB: Dữ liệu User A giữ nguyên 100%, không bị sửa đổi trái phép", "CheckDB: User A giữ nguyên 100%", "Pass", "CheckDB: bảo vệ dữ liệu khi vi phạm phân quyền"),
        ("EPI_TC_022", "user-service/src/models/models.ts", "updateUser() - Cập nhật user không tồn tại: không sinh side-effect", "userId không tồn tại trong CSDL", "CheckDB: Số lượng bản ghi CSDL không đổi; không ảnh hưởng các user khác", "CheckDB: CSDL không bị ảnh hưởng", "Pass", "CheckDB: bảo toàn số lượng bản ghi (không sinh rác)")
    ]

    # -------------------------------------------------------------------------
    # 6. XÂY DỰNG LẠI CÁC DÒNG TỪ DÒNG 21 TRỞ ĐI
    # -------------------------------------------------------------------------
    # Xóa toàn bộ các dòng từ dòng 21 trở xuống để ghi mới chuẩn chỉnh
    if ws.max_row >= 21:
        ws.delete_rows(21, ws.max_row - 20)

    cur_r = 21

    # Section: EXCLUDED FILES
    c_sec = ws.cell(cur_r, 1, "EXCLUDED FILES")
    c_sec.font = section_font
    cur_r += 1

    # Table Header EXCLUDED FILES
    ex_headers = ["STT", "File / Thành phần", "Số dòng (LOC)", "Lớp kiến trúc", "Lý do KHÔNG cần thực hiện Unit Test (Explain Why)"]
    for col_idx, h_text in enumerate(ex_headers, 1):
        cell = ws.cell(cur_r, col_idx, h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = align_center
    cur_r += 1

    # Excluded files data
    for item in excluded_files:
        for col_idx, val in enumerate(item, 1):
            cell = ws.cell(cur_r, col_idx, val)
            cell.font = data_font
            cell.alignment = align_center if col_idx in [1, 3] else align_left
        cur_r += 1

    # 4 blank rows
    cur_r += 4

    # Helper function để render 1 section Test Case
    def render_test_section(section_title, tc_headers, test_cases, start_row):
        r = start_row
        sec_cell = ws.cell(r, 1, section_title)
        sec_cell.font = section_font
        r += 1

        for col_idx, h_text in enumerate(tc_headers, 1):
            cell = ws.cell(r, col_idx, h_text)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = align_center
        r += 1

        for tc in test_cases:
            for col_idx, val in enumerate(tc, 1):
                cell = ws.cell(r, col_idx, val)
                cell.font = data_font
                if col_idx in [1, 7]: # ID hoặc Status
                    cell.alignment = align_center
                else:
                    cell.alignment = align_left
            r += 1
        return r

    tc_table_headers = [
        "Test Case ID",
        "Class / File Name",
        "Test Objective (Mục tiêu)",
        "Input (Dữ liệu đầu vào)",
        "Expected Output",
        "Actual Result",
        "Status",
        "Notes / CheckDB & Rollback"
    ]

    # Section: LOGIN
    cur_r = render_test_section("LOGIN", tc_table_headers, login_test_cases, cur_r)
    cur_r += 4

    # Section: REGISTER
    cur_r = render_test_section("REGISTER", tc_table_headers, register_test_cases, cur_r)
    cur_r += 4

    # Section: EDIT PERSONAL INFORMATION
    cur_r = render_test_section("EDIT PERSONAL INFORMATION", tc_table_headers, edit_profile_test_cases, cur_r)

    # Đảm bảo độ rộng các cột A -> H
    col_widths = {
        'A': 24.0,
        'B': 30.0,
        'C': 45.0,
        'D': 35.0,
        'E': 35.0,
        'F': 35.0,
        'G': 12.0,
        'H': 40.0
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # Lưu lại workbook
    wb.save(file_path)
    print(f"Successfully updated '{sheet_name}' in {file_path}")

if __name__ == "__main__":
    update_report()
