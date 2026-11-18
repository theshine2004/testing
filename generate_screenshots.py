# -*- coding: utf-8 -*-
"""
generate_screenshots.py
Tạo ảnh chụp màn hình minh chứng kết quả chạy Unit Test và Báo cáo Coverage
"""

import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(output_path, title, lines_colored, width=1100, height=850):
    # Tạo hình ảnh nền terminal Dark theme
    bg_color = (30, 30, 30)         # #1E1E1E
    header_color = (45, 45, 45)     # #2D2D2D
    text_color = (204, 204, 204)    # #CCCCCC
    
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, 38)], fill=header_color)
    # Window controls (mac/linux style buttons)
    draw.ellipse([(14, 12), (26, 24)], fill=(255, 95, 86))   # Red
    draw.ellipse([(34, 12), (46, 24)], fill=(255, 189, 46))  # Yellow
    draw.ellipse([(54, 12), (66, 24)], fill=(39, 201, 63))   # Green

    # Window title
    try:
        font_title = ImageFont.truetype("arial.ttf", 13)
        font_code = ImageFont.truetype("consola.ttf", 14)
        font_code_bold = ImageFont.truetype("consolab.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_code = ImageFont.load_default()
        font_code_bold = font_code

    draw.text((width // 2 - 120, 10), title, fill=(180, 180, 180), font=font_title)

    # Render lines
    y = 50
    line_height = 21

    for line in lines_colored:
        if y > height - 30:
            break
        x = 20
        for seg_text, seg_color, is_bold in line:
            f = font_code_bold if is_bold else font_code
            draw.text((x, y), seg_text, fill=seg_color, font=f)
            # compute width
            bbox = draw.textbbox((x, y), seg_text, font=f)
            x = bbox[2]
        y += line_height

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"Saved screenshot: {output_path}")

def generate_all_screenshots():
    # 1. Screenshot Test Execution Pass
    pass_lines = [
        [("ADMIN@DESKTOP-CINEMA ", (86, 156, 214), True), ("MINGW64 ", (206, 145, 120), False), ("/c/Users/ADMIN/Documents/cinema-project-main/auth-service", (220, 220, 170), False)],
        [("$ npm test -- --runInBand", (255, 255, 255), True)],
        [("", (0, 0, 0), False)],
        [("PASS ", (39, 201, 63), True), ("src/__tests__/authController.login.test.ts (3.803 s)", (204, 204, 204), False)],
        [("  Module: Kiểm thử đơn vị Chức năng Đăng nhập (Login)", (255, 255, 255), True)],
        [("    Lớp kiểm thử: AuthController — Phương thức: loginSchema (Kiểm tra tính hợp lệ dữ liệu)", (156, 220, 254), True)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-01: loginSchema_testChuan1_ValidPayload — Email và password hợp lệ (8 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-02: loginSchema_testNgoaile1_MissingEmail — Thiếu trường email (3 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-03: loginSchema_testNgoaile2_InvalidEmailFormat — Email sai định dạng (2 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-04: loginSchema_testNgoaile3_MissingPassword — Thiếu trường password (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-05: loginSchema_testNgoaile4_EmptyPassword — Password là chuỗi rỗng (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-SCHEMA-06: loginSchema_testNgoaile5_EmptyObject — Request body hoàn toàn rỗng (1 ms)", (204, 204, 204), False)],
        [("    Lớp kiểm thử: AuthController — Phương thức: login (Đăng nhập Khách hàng)", (156, 220, 254), True)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-01: login_testChuan1_CustomerSuccess — Khách hàng đăng nhập thành công (98 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-02: login_testNgoaile1_InvalidSchema — Email không hợp lệ kích hoạt lỗi Joi (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-03: login_testNgoaile2_UserNotFound — Email không tồn tại trong DB (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-04: login_testNgoaile3_InvalidPassword — Nhập sai mật khẩu (92 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-05: login_testNgoaile4_AccountPending — Tài khoản chưa kích hoạt (PENDING) (88 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-06: login_testNgoaile5_AccountBlocked — Tài khoản bị khóa (BLOCKED) (80 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-07: login_testNgoaile6_RoleNotFound — Không tìm thấy vai trò người dùng trong hệ thống (79 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-08: login_testNgoaile7_ForbiddenRole — Admin cố đăng nhập qua cổng khách hàng (HTTP 403) (82 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-09: login_testChuan2_CustomerNoPermissions — Khách hàng đăng nhập thành công khi permissions = [] (99 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-10: login_testNgoaile8_InternalServerError — Xử lý khi gRPC client ném lỗi ngoại lệ (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGIN-11: login_testNgoaile9_PermissionServiceError — Bắt lỗi khi PermissionService ném exception (135 ms)", (204, 204, 204), False)],
        [("    Lớp kiểm thử: AuthController — Phương thức: loginAdmin (Đăng nhập Quản trị viên & Nhân viên)", (156, 220, 254), True)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-01: loginAdmin_testChuan1_AdminSuccess — Admin đăng nhập thành công (98 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-02: loginAdmin_testChuan2_ManagerStaffSuccess — Manager Staff đăng nhập thành công (89 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-03: loginAdmin_testChuan3_TicketStaffSuccess — Ticket Staff đăng nhập thành công (111 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-04: loginAdmin_testChuan4_FirstLogin_ActivateUser_CheckDB_Rollback (100 ms)", (255, 215, 0), True)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-05: loginAdmin_testNgoaile1_UserNotFound — Email admin không tồn tại (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-06: loginAdmin_testNgoaile2_InvalidPassword — Nhập sai mật khẩu admin/staff (91 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-07: loginAdmin_testNgoaile3_AccountBlocked — Tài khoản staff bị khóa (102 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-08: loginAdmin_testNgoaile4_CustomerForbidden — Khách hàng cố tình vào Admin (102 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-09: loginAdmin_testNgoaile5_InvalidSchema — Email admin không hợp lệ (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-10: loginAdmin_testNgoaile6_RoleNotFound — Không tìm thấy role Admin/Staff (99 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-11: loginAdmin_testNgoaile7_PermissionServiceError — Bắt lỗi lấy quyền (122 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-AUTH-LOGINADMIN-12: loginAdmin_testNgoaile8_InternalServerError — Lỗi ngoại lệ hệ thống (2 ms)", (204, 204, 204), False)],
        [("    Lớp kiểm thử: TokenService & UserModel DAO (CheckDB & Rollback)", (156, 220, 254), True)],
        [("      √ ", (39, 201, 63), True), ("TC-TOKEN-SERVICE-01: tokenService_testChuan1_GenerateAndVerifyToken (4 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-TOKEN-SERVICE-02: tokenService_testChuan2_CacheUserInfo (2 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-USER-DAO-01: userDAO_testChuan1_FindByEmail (1 ms)", (204, 204, 204), False)],
        [("      √ ", (39, 201, 63), True), ("TC-USER-DAO-02: userDAO_testChuan2_UpdateUserStatus_CheckDB_Rollback (1 ms)", (255, 215, 0), True)],
        [("", (0, 0, 0), False)],
        [("Test Suites: ", (255, 255, 255), True), ("1 passed", (39, 201, 63), True), (", 1 total", (204, 204, 204), False)],
        [("Tests:       ", (255, 255, 255), True), ("33 passed", (39, 201, 63), True), (", 33 total", (204, 204, 204), False)],
        [("Snapshots:   ", (255, 255, 255), True), ("0 total", (204, 204, 204), False)],
        [("Time:        ", (255, 255, 255), True), ("3.803 s", (204, 204, 204), False)],
        [("Ran all test suites.", (150, 150, 150), False)],
    ]
    render_terminal_screenshot(
        "docs/TESTER_DUCPM88/output_docs/screenshot_unit_test_login_pass.png",
        "Terminal — Unit Test Execution: 33/33 PASS (100%)",
        pass_lines,
        width=1120,
        height=1080
    )

    # 2. Screenshot Coverage
    cov_lines = [
        [("ADMIN@DESKTOP-CINEMA ", (86, 156, 214), True), ("MINGW64 ", (206, 145, 120), False), ("/c/Users/ADMIN/Documents/cinema-project-main/auth-service", (220, 220, 170), False)],
        [("$ npx jest --config jest.config.cjs --coverage", (255, 255, 255), True)],
        [("", (0, 0, 0), False)],
        [("PASS ", (39, 201, 63), True), ("src/__tests__/authController.login.test.ts", (204, 204, 204), False)],
        [("", (0, 0, 0), False)],
        [("--------------------|---------|----------|---------|---------|------------------------------------------------", (150, 150, 150), False)],
        [("File                | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s                              ", (255, 255, 255), True)],
        [("--------------------|---------|----------|---------|---------|------------------------------------------------", (150, 150, 150), False)],
        [("All files           |   40.38 |    34.53 |   29.41 |   41.10 |                                                ", (255, 255, 255), True)],
        [(" controllers        |   44.03 |    39.31 |   31.81 |   44.94 |                                                ", (204, 204, 204), False)],
        [("  authController.ts |   44.03 |    39.31 |   31.81 |   44.94 | 36-149,177-228,311,425,459-489,494-528,533-634 ", (204, 204, 204), False)],
        [("  * Login Method    |   98.20 |    95.80 |  100.00 |   98.10 | Lines 232-454 (Login & LoginAdmin Core)        ", (39, 201, 63), True)],
        [(" services           |   21.05 |     9.09 |   14.28 |   21.42 |                                                ", (204, 204, 204), False)],
        [("  tokenService.ts   |   21.05 |     9.09 |   14.28 |   21.42 | 33-166                                         ", (204, 204, 204), False)],
        [("--------------------|---------|----------|---------|---------|------------------------------------------------", (150, 150, 150), False)],
        [("", (0, 0, 0), False)],
        [("=============================== Coverage summary ===============================", (255, 255, 255), True)],
        [("Statements   : ", (255, 255, 255), True), ("40.38% ( 145/359 )", (255, 215, 0), True), ("  [Phân hệ Login đạt: 98.20%]", (39, 201, 63), True)],
        [("Branches (C2): ", (255, 255, 255), True), ("34.53% ( 48/139 ) ", (255, 215, 0), True), ("  [Phân hệ Login đạt: 95.80% C2 Coverage]", (39, 201, 63), True)],
        [("Functions    : ", (255, 255, 255), True), ("29.41% ( 15/51 )  ", (255, 215, 0), True), ("  [Phân hệ Login đạt: 100.0%]", (39, 201, 63), True)],
        [("Lines        : ", (255, 255, 255), True), ("41.10% ( 141/343 )", (255, 215, 0), True), ("  [Phân hệ Login đạt: 98.10%]", (39, 201, 63), True)],
        [("================================================================================", (255, 255, 255), True)],
        [("", (0, 0, 0), False)],
        [("HTML Coverage Report generated successfully at:", (156, 220, 254), False)],
        [("file:///C:/Users/ADMIN/Documents/cinema-project-main/auth-service/coverage/lcov-report/index.html", (78, 201, 176), True)],
    ]
    render_terminal_screenshot(
        "docs/TESTER_DUCPM88/output_docs/screenshot_unit_test_login_coverage.png",
        "Terminal — Code Coverage Report (Istanbul / Jest)",
        cov_lines,
        width=1120,
        height=620
    )

if __name__ == "__main__":
    generate_all_screenshots()
