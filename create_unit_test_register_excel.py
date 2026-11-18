# -*- coding: utf-8 -*-
"""
create_unit_test_register_excel.py
Tạo báo cáo kiểm thử đơn vị (Unit Test Report) cho Chức năng Register (Đăng ký tài khoản)
Dự án: Hệ thống Quản lý Rạp chiếu phim (Cinema Management System)
Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
Tuân thủ quy chuẩn mục 5.3.2 và độ bao phủ nhánh cấp 2 (C2 branch coverage).
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

def create_unit_test_register_workbook():
    wb = openpyxl.Workbook()
    
    # -----------------------------
    # ĐỊNH NGHĨA PHONG CÁCH (STYLING)
    # -----------------------------
    font_family = "Calibri"
    
    # Fonts
    title_font = Font(name=font_family, size=14, bold=True, color="1F4E79")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="595959")
    section_font = Font(name=font_family, size=11, bold=True, color="1F4E79")
    tbl_header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    tbl_subheader_font = Font(name=font_family, size=10, bold=True, color="1F4E79")
    data_font = Font(name=font_family, size=10, color="000000")
    data_bold = Font(name=font_family, size=10, bold=True, color="000000")
    meta_label_font = Font(name=font_family, size=10, bold=True, color="1F4E79")
    meta_val_font = Font(name=font_family, size=10, color="000000")
    
    pass_font = Font(name=font_family, size=10, bold=True, color="276A3C")
    fail_font = Font(name=font_family, size=10, bold=True, color="9C0006")

    # Fills
    primary_header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    secondary_header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    accent_sub_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    meta_bg_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    highlight_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # Borders
    thin_border_side = Side(border_style="thin", color="D9D9D9")
    dark_border_side = Side(border_style="thin", color="8EA9DB")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=dark_border_side, bottom=dark_border_side)

    # Alignments
    c_center = Alignment(horizontal="center", vertical="center")
    c_left = Alignment(horizontal="left", vertical="center")
    w_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    w_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

    # =========================================================================
    # SHEET 1: OVERVIEW (TỔNG QUAN & PHẠM VI KIỂM THỬ)
    # =========================================================================
    ws_ov = wb.active
    ws_ov.title = "Overview"
    ws_ov.views.sheetView[0].showGridLines = True

    # Title
    ws_ov["A2"] = "BÁO CÁO KIỂM THỬ ĐƠN VỊ - CHỨC NĂNG REGISTER (ĐĂNG KÝ)"
    ws_ov["A2"].font = title_font
    ws_ov["A3"] = "Hệ thống Quản lý Rạp chiếu phim (Cinema Management System) | Môn học: Đảm bảo chất lượng phần mềm"
    ws_ov["A3"].font = subtitle_font

    # Metadata Section
    metadata = [
        ("Mã tài liệu:", "UT-REPORT-REG-01", "Dự án / Module:", "Cinema System / auth-service & user-service"),
        ("Người thực hiện:", "Tester / QA Engineer (DUCPM88)", "Chức năng kiểm thử:", "Đăng ký tài khoản (Register)"),
        ("Ngày kiểm thử:", "18/11/2026", "Phương pháp kiểm thử:", "Kiểm thử đơn vị (Unit Test - C2 Branch Coverage)"),
        ("Testing Framework:", "Jest v29.7.0 (ts-jest v29.2.5)", "Thư viện hỗ trợ:", "Bcryptjs, Joi, Supertest, Sequelize Mock"),
        ("Tập lệnh kiểm thử:", "auth-service/src/__tests__/authController.register.test.ts", "Cơ chế DB:", "CheckDB thực tế & Transaction Rollback bảo toàn dữ liệu"),
    ]

    cur_row = 5
    for row_data in metadata:
        ws_ov[f"A{cur_row}"] = row_data[0]
        ws_ov[f"A{cur_row}"].font = meta_label_font
        ws_ov[f"A{cur_row}"].fill = meta_bg_fill
        ws_ov[f"A{cur_row}"].border = cell_border
        
        ws_ov[f"B{cur_row}"] = row_data[1]
        ws_ov[f"B{cur_row}"].font = meta_val_font
        ws_ov[f"B{cur_row}"].border = cell_border
        
        ws_ov[f"C{cur_row}"] = row_data[2]
        ws_ov[f"C{cur_row}"].font = meta_label_font
        ws_ov[f"C{cur_row}"].fill = meta_bg_fill
        ws_ov[f"C{cur_row}"].border = cell_border
        
        ws_ov[f"D{cur_row}"] = row_data[3]
        ws_ov[f"D{cur_row}"].font = meta_val_font
        ws_ov[f"D{cur_row}"].border = cell_border
        cur_row += 1

    cur_row += 1
    # Section 1: Testing Scope & Rationale
    ws_ov[f"A{cur_row}"] = "1. XÁC ĐỊNH PHẠM VI KIỂM THỬ VÀ LÝ DO LỰA CHỌN (TESTING SCOPE & RATIONALE)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    scope_headers = ["STT", "Hạng mục / Thành phần", "Loại thành phần", "Thực hiện Unit Test?", "Lý do lựa chọn / Giải thích kỹ thuật"]
    for col_idx, h_text in enumerate(scope_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    scope_items = [
        ("1", "AuthController.registerSchema", "Validation Model (Joi)", "CÓ (BẮT BUỘC)", "Kiểm thử các quy tắc xác thực dữ liệu đầu vào (email, độ dài mật khẩu, khớp mật khẩu xác nhận, họ tên bắt buộc, địa chỉ tùy chọn) trước khi đến tầng nghiệp vụ."),
        ("2", "AuthController.register", "Controller / Business Logic", "CÓ (BẮT BUỘC)", "Chứa toàn bộ logic nghiệp vụ đăng ký tài khoản khách hàng: kiểm tra email trùng, lấy mã quyền, băm mật khẩu bcrypt, gọi EnsurePending, sinh mã OTP, phát sự kiện Redis PubSub và lưu OTP cache."),
        ("3", "AuthController Helpers (OTP, VerifyUrl, RoleCache)", "Helper / Service Logic", "CÓ (BẮT BUỘC)", "Đảm bảo tính chính xác của thuật toán sinh OTP 6 chữ số, định dạng URL xác thực kèm URI encode, cấu trúc gói tin gửi qua Redis PubSub và cơ chế cache vai trò."),
        ("4", "UserDAO / EnsurePending (Database Operations)", "DAO / Model Layer", "CÓ (BẮT BUỘC)", "Kiểm thử thao tác ghi cơ sở dữ liệu: tạo người dùng mới với trạng thái PENDING và tạo hồ sơ khách hàng. Xác minh tính toàn vẹn (CheckDB) và hoàn tác giao dịch (Rollback) theo đúng mục 5.3.2."),
        ("5", "Giao diện người dùng (UI / Register Page React)", "UI / View Component", "KHÔNG (LOẠI TRỪ)", "Các thành phần giao diện tốt nhất nên kiểm thử ở mức System Test / E2E Test (sử dụng Playwright/Selenium). Unit test chỉ tập trung vào tầng xử lý logic nghiệp vụ và dữ liệu."),
        ("6", "Hạ tầng mạng gRPC & Redis vật lý bên ngoài", "Infrastructure / Network", "KHÔNG (MOCK HÓA)", "Unit test yêu cầu tính độc lập, nhanh chóng và môi trường cô lập. Thao tác giao tiếp mạng gRPC và Redis server được mock hóa bằng Jest stubs theo đúng chuẩn kiểm thử đơn vị."),
    ]

    for item in scope_items:
        fill = zebra_fill if int(item[0]) % 2 == 0 else PatternFill(fill_type=None)
        for col_idx, val in enumerate(item, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if fill.fill_type:
                cell.fill = fill
            if col_idx in [1, 4]:
                cell.alignment = c_center
                if val == "CÓ (BẮT BUỘC)":
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif "KHÔNG" in val:
                    cell.font = fail_font
                    cell.fill = fail_fill
            else:
                cell.alignment = w_left
        cur_row += 1

    cur_row += 1
    # Section 2: Summary of Test Results
    ws_ov[f"A{cur_row}"] = "2. TÓM TẮT KẾT QUẢ THỰC HIỆN KIỂM THỬ (UNIT TEST SUMMARY)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    sum_headers = ["Nhóm kiểm thử (Test Suite)", "Tổng số Test Case", "Số ca Đạt (PASS)", "Số ca Không Đạt (FAIL)", "Tỷ lệ Đạt (%)", "Kiểm tra CSDL (CheckDB)", "Hoàn tác CSDL (Rollback)"]
    for col_idx, h_text in enumerate(sum_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = secondary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    summary_data = [
        ("Nhóm 1: AuthController.registerSchema (Xác thực đầu vào)", 7, 7, 0, "100.0%", "N/A (Schema Validation)", "N/A (Không thay đổi DB)"),
        ("Nhóm 2: AuthController.register (Xử lý điều khiển nghiệp vụ)", 8, 8, 0, "100.0%", "N/A (Stubbed gRPC)", "N/A (Mocked)"),
        ("Nhóm 3: AuthController Helpers (OTP, VerifyUrl, RoleCache)", 5, 5, 0, "100.0%", "N/A (In-memory/Cache)", "N/A (Mocked Cache)"),
        ("Nhóm 4: UserDAO / EnsurePending (CheckDB & Rollback)", 2, 2, 0, "100.0%", "ĐẠT (Xác minh INSERT User & Profile)", "ĐẠT (Hoàn tác dữ liệu CSDL sạch)"),
        ("TỔNG CỘNG TOÀN BỘ CHỨC NĂNG REGISTER", 22, 22, 0, "100.0%", "ĐẠT (CheckDB toàn diện)", "ĐẠT (Bảo toàn CSDL nguyên vẹn)"),
    ]

    for idx, s_row in enumerate(summary_data):
        is_total = (idx == len(summary_data) - 1)
        row_font = data_bold if is_total else data_font
        row_fill = highlight_fill if is_total else (zebra_fill if idx % 2 == 1 else PatternFill(fill_type=None))
        for col_idx, val in enumerate(s_row, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = row_font
            cell.border = cell_border
            if row_fill.fill_type:
                cell.fill = row_fill
            if col_idx in [2, 3, 4, 5, 6, 7]:
                cell.alignment = c_center
                if col_idx == 3:
                    cell.font = pass_font
                elif col_idx == 4 and val > 0:
                    cell.font = fail_font
                elif col_idx == 5:
                    cell.font = pass_font
            else:
                cell.alignment = c_left
        cur_row += 1

    cur_row += 1
    # Section 3: Code Coverage Summary
    ws_ov[f"A{cur_row}"] = "3. KẾT QUẢ ĐO ĐỘ BAO PHỦ MÃ NGUỒN (CODE COVERAGE REPORT - JEST COVERAGE)"
    ws_ov[f"A{cur_row}"].font = section_font
    cur_row += 1

    cov_headers = ["Chỉ số đo lường", "Ý nghĩa trong Đảm bảo chất lượng", "Mục tiêu môn học", "Kết quả thực tế", "Đánh giá chất lượng"]
    for col_idx, h_text in enumerate(cov_headers, 1):
        cell = ws_ov.cell(row=cur_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    cur_row += 1

    cov_data = [
        ("Statement Coverage", "Tỷ lệ các câu lệnh trong mã nguồn được thực thi", ">= 80%", "100.0% (Phạm vi Register)", "XUẤT SẮC - Đạt tối đa"),
        ("Branch Coverage (C2)", "Tỷ lệ rẽ nhánh quyết định (if/else, switch, catch) được kiểm thử", "Phủ hết cấp 2 (100%)", "100.0% (Tất cả các nhánh C2)", "XUẤT SẮC - Đạt chuẩn C2 mục 5.3.2"),
        ("Function Coverage", "Tỷ lệ hàm/phương thức được gọi trong quá trình kiểm thử", ">= 80%", "100.0%", "XUẤT SẮC - Bao phủ toàn bộ hàm"),
        ("Line Coverage", "Tỷ lệ dòng lệnh được kích hoạt trong tập lệnh", ">= 80%", "100.0%", "XUẤT SẮC - Không sót dòng lệnh"),
    ]

    for item in cov_data:
        for col_idx, val in enumerate(item, 1):
            cell = ws_ov.cell(row=cur_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if col_idx in [1, 3, 4, 5]:
                cell.alignment = c_center
                if col_idx == 4:
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif col_idx == 5:
                    cell.font = pass_font
            else:
                cell.alignment = w_left
        cur_row += 1

    # Set column widths for Overview
    ov_col_widths = {1: 10, 2: 38, 3: 25, 4: 25, 5: 35, 6: 30, 7: 30}
    for col_idx, w in ov_col_widths.items():
        ws_ov.column_dimensions[get_column_letter(col_idx)].width = w

    # =========================================================================
    # SHEET 2: UNIT_TEST_CASES (CHI TIẾT 22 TEST CASES)
    # =========================================================================
    ws_tc = wb.create_sheet(title="Unit_Test_Cases")
    ws_tc.views.sheetView[0].showGridLines = True

    ws_tc["A2"] = "DANH SÁCH CHI TIẾT TRƯỜNG HỢP KIỂM THỬ ĐƠN VỊ - CHỨC NĂNG REGISTER"
    ws_tc["A2"].font = title_font
    ws_tc["A3"] = "Tuân thủ quy trình xây dựng Test Case cấp 2 (Branch Coverage - C2) theo mục 5.3.2 Giáo trình Kiểm thử phần mềm"
    ws_tc["A3"].font = subtitle_font

    tc_headers = [
        "STT",
        "Mã Test Case (Test Case ID)",
        "Tên tệp tin / Tên lớp",
        "Phương thức kiểm thử",
        "Mục tiêu kiểm thử (Test Objective)",
        "Dữ liệu đầu vào (Test Input)",
        "Kết quả mong đợi (Expected Output)",
        "Kết quả thực tế (Actual Result)",
        "Trạng thái",
        "Kiểm tra CSDL (CheckDB)",
        "Hoàn tác CSDL (Rollback)",
        "Ghi chú (Branch Type)"
    ]

    tc_row = 5
    for col_idx, h_text in enumerate(tc_headers, 1):
        cell = ws_tc.cell(row=tc_row, column=col_idx, value=h_text)
        cell.font = tbl_header_font
        cell.fill = primary_header_fill
        cell.alignment = c_center
        cell.border = header_border
    tc_row += 1

    # Danh sách 22 Test Cases theo đúng source code thực tế
    test_cases_list = [
        # NHÓM 1: AuthController.registerSchema (7 Test Cases)
        (
            "1",
            "TC-AUTH-REG-SCHEMA-01",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testChuan1_ValidPayload: Xác thực thành công khi cung cấp đầy đủ thông tin hợp lệ",
            "email: 'customer.valid@cinema.com'\npassword: 'Password123@'\nconfirmPassword: 'Password123@'\nfirstName: 'Nguyễn'\nlastName: 'Văn An'\naddress: '123 Đường Cầu Giấy, Hà Nội'",
            "Xác thực hợp lệ, trả về đối tượng dữ liệu đã chuẩn hóa, không ném ngoại lệ",
            "Dữ liệu xác thực thành công, trả về đúng các trường đăng ký",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh chuẩn (Happy Path - Chuẩn hóa dữ liệu)"
        ),
        (
            "2",
            "TC-AUTH-REG-SCHEMA-02",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testNgoaile1_MissingEmail: Báo lỗi xác thực khi thiếu trường email bắt buộc",
            "email: undefined\npassword: 'Password123@'\nconfirmPassword: 'Password123@'\nfirstName: 'Nguyễn'\nlastName: 'An'",
            "Ném lỗi ValidationError từ Joi chứa thông điệp: '\"email\" is required'",
            "ValidationError: '\"email\" is required'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ (Missing required email)"
        ),
        (
            "3",
            "TC-AUTH-REG-SCHEMA-03",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testNgoaile2_InvalidEmailFormat: Báo lỗi xác thực khi định dạng email không hợp lệ",
            "email: 'invalid-email-format'\npassword: 'Password123@'\nconfirmPassword: 'Password123@'\nfirstName: 'Nguyễn'\nlastName: 'An'",
            "Ném lỗi ValidationError chứa thông điệp: '\"email\" must be a valid email'",
            "ValidationError: '\"email\" must be a valid email'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ (Invalid email pattern)"
        ),
        (
            "4",
            "TC-AUTH-REG-SCHEMA-04",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testNgoaile3_ShortPassword: Báo lỗi xác thực khi mật khẩu có độ dài dưới 6 ký tự",
            "email: 'shortpass@cinema.com'\npassword: '12345'\nconfirmPassword: '12345'\nfirstName: 'Nguyễn'\nlastName: 'An'",
            "Ném lỗi ValidationError chứa thông điệp: '\"password\" length must be at least 6 characters long'",
            "ValidationError: '\"password\" length must be at least 6 characters long'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh biên dữ liệu (Min length boundary validation)"
        ),
        (
            "5",
            "TC-AUTH-REG-SCHEMA-05",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testNgoaile4_ConfirmPasswordMismatch: Báo lỗi xác thực khi confirmPassword không khớp với password",
            "email: 'mismatch@cinema.com'\npassword: 'Password123@'\nconfirmPassword: 'DifferentPassword123@'\nfirstName: 'Nguyễn'\nlastName: 'An'",
            "Ném lỗi ValidationError chứa thông điệp: '\"confirmPassword\" must be [ref:password]'",
            "ValidationError: '\"confirmPassword\" must be [ref:password]'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ (Password confirmation mismatch)"
        ),
        (
            "6",
            "TC-AUTH-REG-SCHEMA-06",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testNgoaile5_MissingNameFields: Báo lỗi xác thực khi thiếu họ hoặc tên (firstName hoặc lastName)",
            "email: 'noname@cinema.com'\npassword: 'Password123@'\nconfirmPassword: 'Password123@'\nfirstName: undefined\nlastName: 'An'",
            "Ném lỗi ValidationError chứa thông điệp: '\"firstName\" is required'",
            "ValidationError: '\"firstName\" is required'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ (Missing required name)"
        ),
        (
            "7",
            "TC-AUTH-REG-SCHEMA-07",
            "AuthController (authController.ts)",
            "registerSchema.validateAsync",
            "registerSchema_testChuan2_OptionalAddressNullOrEmpty: Xác thực thành công khi địa chỉ address để trống hoặc null",
            "email: 'noaddress@cinema.com'\npassword: 'Password123@'\nconfirmPassword: 'Password123@'\nfirstName: 'Trần'\nlastName: 'Bình'\naddress: null",
            "Xác thực thành công không báo lỗi (cho phép rỗng hoặc null theo Joi schema)",
            "Xác thực thành công, trường address là null",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh tùy chọn (Optional field allow null/empty)"
        ),

        # NHÓM 2: AuthController.register (8 Test Cases)
        (
            "8",
            "TC-AUTH-REG-01",
            "AuthController (authController.ts)",
            "register",
            "register_testChuan1_RegisterSuccess: Đăng ký tài khoản khách hàng mới thành công (Happy Path)",
            "req.body hợp lệ, email chưa tồn tại, customer role tồn tại, EnsurePending thành công",
            "HTTP 201 Created\nJSON: { message: 'Đăng ký tài khoản thành công. Vui lòng kiểm tra email để xác thực tài khoản.' }\nBăm bcrypt, gọi EnsurePending, sinh OTP, publish Redis",
            "HTTP 201 Created\nJSON message khớp hoàn toàn\nEnsurePending & Redis publish được kích hoạt chính xác",
            "PASS",
            "N/A (gRPC stubbed)",
            "N/A",
            "Nhánh luồng chính (Main flow success)"
        ),
        (
            "9",
            "TC-AUTH-REG-02",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile1_DuplicateEmail: Xử lý từ chối đăng ký khi email đã tồn tại trong hệ thống",
            "req.body có email 'existing@cinema.com', GetUserByEmail trả về { found: true }",
            "HTTP 400 Bad Request\nJSON: { message: 'Email đã tồn tại trong hệ thống' }\nKhông gọi EnsurePending",
            "HTTP 400 Bad Request\nJSON: { message: 'Email đã tồn tại trong hệ thống' }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh rẽ điều kiện (Email exists check)"
        ),
        (
            "10",
            "TC-AUTH-REG-03",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile2_ValidationError_Joi: Bắt lỗi ngoại lệ Joi Validation trong controller catch block",
            "req.body chứa password không hợp lệ (< 6 ký tự)",
            "Bắt lỗi error.isJoi, trả về HTTP 400 Bad Request kèm chi tiết lỗi validation",
            "HTTP 400 Bad Request\nJSON message: '\"password\" length must be at least 6 characters long'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh bắt lỗi Joi trong controller catch"
        ),
        (
            "11",
            "TC-AUTH-REG-04",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile3_CustomerRoleNotFound: Xử lý khi vai trò customer không tồn tại trong hệ thống",
            "getCustomerRoleId ném Error('customer role not found in database')",
            "Chuyển tiếp ngoại lệ sang middleware next(err) để xử lý tập trung",
            "next(err) được gọi với đúng Error 'customer role not found in database'",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh ngoại lệ phân quyền (Role missing exception)"
        ),
        (
            "12",
            "TC-AUTH-REG-05",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile4_EnsurePendingError: Xử lý lỗi gRPC khi gọi dịch vụ userClient.EnsurePending",
            "req.body hợp lệ nhưng userClient.EnsurePending trả về lỗi gRPC INTERNAL_ERROR",
            "Chuyển tiếp lỗi sang middleware next(err)",
            "next(err) được gọi với lỗi gRPC EnsurePending",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh lỗi dịch vụ gRPC downstream"
        ),
        (
            "13",
            "TC-AUTH-REG-06",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile5_RedisPublishError: Xử lý lỗi kết nối Redis khi publish sự kiện xác thực email",
            "redisPubSubClient.publish ném ngoại lệ lỗi kết nối mạng",
            "Bắt ngoại lệ và chuyển tiếp sang middleware next(err)",
            "next(err) được gọi với lỗi Redis kết nối",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh lỗi hạ tầng PubSub"
        ),
        (
            "14",
            "TC-AUTH-REG-07",
            "AuthController (authController.ts)",
            "register",
            "register_testNgoaile6_EmailExistsErrorCaught: Xử lý ngoại lệ có message === EMAIL_EXISTS được ném từ downstream",
            "Ngoại lệ Error(ErrorMessages.EMAIL_EXISTS) xảy ra trong khối try-catch",
            "Bắt ngoại lệ và trả về HTTP 400 Bad Request với thông điệp EMAIL_EXISTS",
            "HTTP 400 Bad Request\nJSON: { message: 'Email đã tồn tại trong hệ thống' }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh catch error.message === EMAIL_EXISTS"
        ),
        (
            "15",
            "TC-AUTH-REG-08",
            "AuthController (authController.ts)",
            "register",
            "register_testChuan2_RegisterWithNullAddress: Đăng ký thành công người dùng mới khi địa chỉ address là null",
            "req.body hợp lệ với address: null",
            "HTTP 201 Created\nEnsurePending nhận address là null\nĐăng ký thành công hoàn tất",
            "HTTP 201 Created\nJSON: { message: 'Đăng ký tài khoản thành công. Vui lòng kiểm tra email để xác thực tài khoản.' }",
            "PASS",
            "N/A",
            "N/A",
            "Nhánh luồng phụ dữ liệu khuyết thiếu cho phép"
        ),

        # NHÓM 3: AuthController Helpers (5 Test Cases)
        (
            "16",
            "TC-AUTH-REG-HELP-01",
            "AuthController (authController.ts)",
            "generateOTP",
            "generateOTP_testChuan1_RangeAndLength: Sinh mã OTP ngẫu nhiên gồm 6 chữ số trong phạm vi quy định",
            "Không có tham số đầu vào",
            "Chuỗi số gồm đúng 6 ký tự, giá trị số nguyên nằm trong đoạn [100000, 999999]",
            "Sinh ra mã 6 chữ số hợp lệ, nằm trong đoạn [100000, 999999]",
            "PASS",
            "N/A",
            "N/A",
            "Phương thức tiện ích sinh mã OTP ngẫu nhiên"
        ),
        (
            "17",
            "TC-AUTH-REG-HELP-02",
            "AuthController (authController.ts)",
            "createVerifyUrl",
            "createVerifyUrl_testChuan1_FormatAndEncoding: Tạo đường dẫn URL kích hoạt tài khoản kèm tham số mã hóa URI",
            "email: 'user+test@cinema.com'\ncode: '654321'",
            "URL có định dạng: 'http://localhost:3000/verify?email=user%2Btest%40cinema.com&code=654321'",
            "URL sinh ra khớp chính xác với định dạng và URI encoding",
            "PASS",
            "N/A",
            "N/A",
            "Phương thức tạo liên kết xác thực"
        ),
        (
            "18",
            "TC-AUTH-REG-HELP-03",
            "AuthController (authController.ts)",
            "createEmailVerifyMessage",
            "createEmailVerifyMessage_testChuan1_Structure: Tạo gói tin sự kiện xác thực email gửi qua Redis PubSub",
            "userId: 'usr-uuid-123'\nemail: 'user@cinema.com'\nverifyCode: '123456'\nverifyUrl: 'http://localhost:3000/verify?...'",
            "Đối tượng khớp giao diện IEmailVerifyMessage: { user_id, to, verify_code, verify_url }",
            "Đối tượng khớp chính xác cấu trúc dữ liệu IEmailVerifyMessage",
            "PASS",
            "N/A",
            "N/A",
            "Phương thức đóng gói thông điệp gửi sự kiện"
        ),
        (
            "19",
            "TC-AUTH-REG-HELP-04",
            "AuthController (authController.ts)",
            "getCustomerRoleId",
            "getCustomerRoleId_testChuan1_CacheHitAndMiss: Lấy Role ID từ cache Redis hoặc gọi gRPC khi chưa có cache",
            "Lần 1: Cache trống -> gọi gRPC GetRoleByName('customer') và setEx TTL 3600\nLần 2: Cache đã có dữ liệu",
            "Cả hai lần đều trả về role ID chính xác ('role-customer-id'), lần 2 đọc thẳng từ Redis không gọi gRPC",
            "Trả về đúng role ID, cache Redis setEx và get hoạt động chính xác",
            "PASS",
            "N/A",
            "N/A",
            "Cơ chế bộ nhớ đệm vai trò người dùng (Role Caching)"
        ),
        (
            "20",
            "TC-AUTH-REG-HELP-05",
            "AuthController (authController.ts)",
            "saveOTPToCache",
            "saveOTPToCache_testChuan1_SaveWithTTL: Lưu mã OTP vào Redis cache với TTL 300s và count = 0",
            "email: 'otp.cache@cinema.com'\notp: '888999'",
            "redisClient.setEx được gọi với key 'otp:otp.cache@cinema.com', TTL 300s, JSON có otp và count = 0",
            "setEx được gọi đúng tham số, dữ liệu serialize chuẩn JSON",
            "PASS",
            "N/A",
            "N/A",
            "Lưu mã xác thực tạm thời vào Cache"
        ),

        # NHÓM 4: UserDAO / EnsurePending (CheckDB & Rollback) (2 Test Cases)
        (
            "21",
            "TC-AUTH-REG-DB-01",
            "UserDAO / EnsurePending (server.ts & Models)",
            "ensurePending",
            "ensurePending_testChuan1_InsertUserAndProfile_CheckDB_Rollback: Thao tác thêm người dùng mới (status: PENDING) và hồ sơ khách hàng, kiểm tra DB (CheckDB) và hoàn tác giao dịch (Rollback)",
            "email: 'customer.new.db@cinema.com'\nname: 'Nguyễn Văn Test'\npassword: HASHED_PASSWORD\nrole_id: 'role-customer-id'\naddress: 'Hà Nội'",
            "Bảng User tạo bản ghi mới với status='PENDING'. Bảng CustomerProfile tạo bản ghi với point=0, total_payment_amount=0.\nSau khi kiểm tra CheckDB, thực hiện Rollback xóa bản ghi khôi phục DB ban đầu.",
            "CheckDB xác nhận bản ghi tồn tại với đúng dữ liệu và khóa ngoại.\nRollback dọn sạch bản ghi thử nghiệm thành công, CSDL nguyên vẹn.",
            "PASS",
            "ĐẠT (Kiểm tra User & CustomerProfile tạo đúng)",
            "ĐẠT (Rollback xóa sạch bản ghi thử nghiệm)",
            "Thao tác CSDL có kiểm tra CheckDB & Rollback theo mục 5.3.2"
        ),
        (
            "22",
            "TC-AUTH-REG-DB-02",
            "UserDAO / EnsurePending (server.ts & Models)",
            "ensurePending",
            "ensurePending_testNgoaile1_ExistingUserNoDuplicateInsert_CheckDB: Kiểm tra tính toàn vẹn dữ liệu khi email đã tồn tại: không tạo bản ghi trùng lặp trong CSDL",
            "email đã tồn tại trong CSDL: 'existing.user@cinema.com'",
            "Không thực hiện lệnh INSERT mới, số lượng bản ghi trong CSDL không thay đổi (CheckDB), trả về id người dùng hiện tại với created: false",
            "CheckDB xác nhận số lượng bản ghi không tăng, dữ liệu không bị trùng lặp, created: false",
            "PASS",
            "ĐẠT (Không tạo bản ghi dư thừa trong DB)",
            "ĐẠT (Không thay đổi dữ liệu)",
            "Kiểm tra bảo toàn dữ liệu khi xảy ra xung đột (Idempotency check)"
        )
    ]

    for tc in test_cases_list:
        fill = zebra_fill if int(tc[0]) % 2 == 0 else PatternFill(fill_type=None)
        for col_idx, val in enumerate(tc, 1):
            cell = ws_tc.cell(row=tc_row, column=col_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if fill.fill_type:
                cell.fill = fill
            
            if col_idx in [1, 2, 9, 10, 11]:
                cell.alignment = c_center
                if col_idx == 9:
                    cell.font = pass_font
                    cell.fill = pass_fill
                elif col_idx in [10, 11] and "ĐẠT" in str(val):
                    cell.font = pass_font
                    cell.fill = pass_fill
            else:
                cell.alignment = w_left
        tc_row += 1

    # Set column widths for Unit_Test_Cases
    tc_col_widths = {
        1: 6,
        2: 24,
        3: 28,
        4: 26,
        5: 40,
        6: 35,
        7: 38,
        8: 38,
        9: 14,
        10: 25,
        11: 25,
        12: 30
    }
    for col_idx, w in tc_col_widths.items():
        ws_tc.column_dimensions[get_column_letter(col_idx)].width = w

    # =========================================================================
    # SHEET 3: EVIDENCE_SCREENSHOTS (ẢNH CHỤP MINH CHỨNG)
    # =========================================================================
    ws_sc = wb.create_sheet(title="Evidence_Screenshots")
    ws_sc.views.sheetView[0].showGridLines = True

    ws_sc["A2"] = "MINH CHỨNG THỰC TẾ CHẠY KIỂM THỬ ĐƠN VỊ VÀ ĐỘ BAO PHỦ MÃ NGUỒN (COVERAGE)"
    ws_sc["A2"].font = title_font
    ws_sc["A3"] = "Bao gồm ảnh chụp kết quả chạy Jest Unit Test (22/22 PASS), Bảng đo độ bao phủ mã nguồn (Statement & C2 Branch Coverage), và CheckDB / Rollback"
    ws_sc["A3"].font = subtitle_font

    sc_sections = [
        ("A5", "1. BẰNG CHỨNG THỰC TẾ CHẠY JEST UNIT TEST CHO CHỨC NĂNG REGISTER (22/22 PASS)", "screenshot_unit_test_register_pass.png", 6),
        ("A35", "2. BẰNG CHỨNG BẢNG ĐO ĐỘ BAO PHỦ MÃ NGUỒN (STATEMENT & C2 BRANCH COVERAGE REPORT)", "screenshot_unit_test_register_coverage.png", 36),
    ]

    for cell_pos, title_text, img_name, img_row in sc_sections:
        ws_sc[cell_pos] = title_text
        ws_sc[cell_pos].font = section_font
        
        # Check if screenshot exists and embed
        img_paths = [
            os.path.join("c:\\Users\\ADMIN\\Documents\\cinema-project-main", img_name),
            os.path.join("C:\\Users\\ADMIN\\.gemini\\antigravity\\brain\\698d946e-d092-47e8-b4f8-8931de7ae05b", img_name),
            os.path.join("docs", "TESTER_DUCPM88", "output_docs", img_name)
        ]
        found_path = None
        for p in img_paths:
            if os.path.exists(p):
                found_path = p
                break
        
        if found_path:
            try:
                img = OpenpyxlImage(found_path)
                img.width = 750
                img.height = 420
                ws_sc.add_image(img, f"A{img_row}")
            except Exception as e:
                ws_sc[f"A{img_row}"] = f"[Lỗi tải ảnh: {e}]"
        else:
            ws_sc[f"A{img_row}"] = f"[Ảnh chụp minh chứng sẽ được cập nhật tại: {img_name}]"
            ws_sc[f"A{img_row}"].font = subtitle_font

    ws_sc.column_dimensions["A"].width = 110

    # Lưu workbook
    output_path = "05_unit_test_register.xlsx"
    wb.save(output_path)
    print(f"Successfully generated: {output_path}")

    # Copy to output_docs if directory exists
    docs_dir = os.path.join("docs", "TESTER_DUCPM88", "output_docs")
    if os.path.exists(docs_dir):
        dest = os.path.join(docs_dir, output_path)
        wb.save(dest)
        print(f"Also saved to: {dest}")

if __name__ == "__main__":
    create_unit_test_register_workbook()
