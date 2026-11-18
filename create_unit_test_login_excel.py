# -*- coding: utf-8 -*-
"""
create_unit_test_login_excel.py
Tạo báo cáo kiểm thử đơn vị (Unit Test Report) cho Chức năng Login
Dự án: Hệ thống Quản lý Rạp chiếu phim (Cinema Management System)
Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

def create_unit_test_login_workbook():
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

    # 1. TIÊU ĐỀ
    ws_ov.merge_cells("A1:H1")
    ws_ov.cell(row=1, column=1, value="BÁO CÁO KIỂM THỬ ĐƠN VỊ (UNIT TEST REPORT) — CHỨC NĂNG LOGIN").font = title_font
    ws_ov.cell(row=1, column=1).alignment = c_left
    ws_ov.row_dimensions[1].height = 28

    ws_ov.merge_cells("A2:H2")
    ws_ov.cell(row=2, column=1, value="Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm) | Dự án: Hệ thống Quản lý Rạp chiếu phim").font = subtitle_font
    ws_ov.cell(row=2, column=1).alignment = c_left
    ws_ov.row_dimensions[2].height = 20

    # 2. THÔNG TIN CHUNG
    ws_ov.cell(row=4, column=1, value="I. THÔNG TIN CHUNG").font = section_font
    gen_info = [
        ("Tên dự án:", "Hệ thống Quản lý Rạp chiếu phim (Cinema Management System)"),
        ("Chức năng kiểm thử:", "Đăng nhập người dùng (Login — Customer, Admin & Staff)"),
        ("Khung kiểm thử (Testing Framework):", "Jest v29.7.0 kết hợp ts-jest / Node.js ESM (TypeScript Unit Testing)"),
        ("Thư viện bổ trợ (Libraries):", "bcryptjs, jsonwebtoken (JWT), Joi validation, Sequelize ORM"),
        ("Công cụ đo độ bao phủ (Coverage Tool):", "Istanbul / Jest Coverage (Đo Statements, Branches C2, Functions, Lines)"),
        ("Chiến lược kiểm thử (Testing Strategy):", "Phủ cấp 2 (Branch Coverage - C2), Phân hoạch tương đương, Phân tích giá trị biên, CheckDB & Rollback"),
        ("Môi trường thực thi:", "Node.js v24.11.1 LTS | Hệ điều hành: Windows 11 x64")
    ]
    for idx, (lbl, val) in enumerate(gen_info, start=5):
        ws_ov.row_dimensions[idx].height = 21
        c_lbl = ws_ov.cell(row=idx, column=1, value=lbl)
        c_lbl.font = meta_label_font
        c_lbl.fill = meta_bg_fill
        c_lbl.border = cell_border
        
        ws_ov.merge_cells(start_row=idx, start_column=2, end_row=idx, end_column=7)
        for col_i in range(2, 8):
            c = ws_ov.cell(row=idx, column=col_i)
            c.border = cell_border
            c.fill = meta_bg_fill
        ws_ov.cell(row=idx, column=2, value=val).font = meta_val_font

    # 3. BẢNG THỐNG KÊ KẾT QUẢ KIỂM THỬ
    start_r = 14
    ws_ov.cell(row=start_r, column=1, value="II. BẢNG THỐNG KÊ KẾT QUẢ KIỂM THỬ ĐƠN VỊ").font = section_font
    
    stat_headers = ["STT", "Hạng mục / Phân hệ", "Lớp / Tệp kiểm thử", "Tổng số TC", "PASS", "FAIL", "Tỷ lệ Pass"]
    ws_ov.row_dimensions[start_r + 1].height = 24
    for c_i, h in enumerate(stat_headers, 1):
        c = ws_ov.cell(row=start_r + 1, column=c_i, value=h)
        c.font = tbl_header_font
        c.fill = primary_header_fill
        c.alignment = c_center
        c.border = header_border

    stat_data = [
        (1, "Kiểm tra hợp lệ dữ liệu (Validation)", "AuthController.loginSchema", 6, 6, 0, "100.0%"),
        (2, "Đăng nhập Khách hàng (Customer Login)", "AuthController.login", 11, 11, 0, "100.0%"),
        (3, "Đăng nhập Quản trị & Nhân viên (Admin/Staff)", "AuthController.loginAdmin", 12, 12, 0, "100.0%"),
        (4, "Dịch vụ Token & Phiên làm việc", "TokenService", 2, 2, 0, "100.0%"),
        (5, "Kiểm tra thao tác DB & Rollback", "UserDAO / Sequelize Model", 2, 2, 0, "100.0%"),
    ]

    curr_r = start_r + 2
    for row in stat_data:
        ws_ov.row_dimensions[curr_r].height = 21
        for col_i, val in enumerate(row, 1):
            c = ws_ov.cell(row=curr_r, column=col_i, value=val)
            c.font = data_font
            c.border = cell_border
            if col_i in [1, 4, 5, 6, 7]:
                c.alignment = c_center
            else:
                c.alignment = c_left
            if col_i == 5:
                c.fill = pass_fill
                c.font = pass_font
            elif col_i == 6:
                c.fill = fail_fill if val > 0 else zebra_fill
                c.font = fail_font if val > 0 else data_font
            elif col_i == 7:
                c.fill = pass_fill
                c.font = pass_font
        curr_r += 1

    # Dòng Tổng cộng
    ws_ov.row_dimensions[curr_r].height = 22
    ws_ov.cell(row=curr_r, column=1, value="").border = cell_border
    ws_ov.merge_cells(start_row=curr_r, start_column=1, end_row=curr_r, end_column=3)
    ws_ov.cell(row=curr_r, column=1, value="TỔNG CỘNG").alignment = c_center
    ws_ov.cell(row=curr_r, column=4, value="=SUM(D16:D20)").alignment = c_center
    ws_ov.cell(row=curr_r, column=5, value="=SUM(E16:E20)").alignment = c_center
    ws_ov.cell(row=curr_r, column=6, value="=SUM(F16:F20)").alignment = c_center
    ws_ov.cell(row=curr_r, column=7, value="100.0%").alignment = c_center
    for c_i in range(1, 8):
        c = ws_ov.cell(row=curr_r, column=c_i)
        c.font = data_bold
        c.fill = accent_sub_fill
        c.border = cell_border

    # 4. TÓM TẮT ĐỘ BAO PHỦ MÃ NGUỒN (CODE COVERAGE)
    curr_r += 3
    ws_ov.cell(row=curr_r, column=1, value="III. TÓM TẮT ĐỘ BAO PHỦ MÃ NGUỒN (CODE COVERAGE REPORT)").font = section_font
    cov_headers = ["Tiêu chí đo lường", "Ý nghĩa trong kiểm thử", "Mức phủ phân hệ Login", "Mức phủ toàn Service", "Đánh giá chất lượng"]
    curr_r += 1
    ws_ov.row_dimensions[curr_r].height = 24
    for c_i, h in enumerate(cov_headers, 1):
        c = ws_ov.cell(row=curr_r, column=c_i, value=h)
        c.font = tbl_header_font
        c.fill = secondary_header_fill
        c.alignment = c_center
        c.border = header_border

    cov_data = [
        ("% Statement Coverage", "Tỷ lệ các câu lệnh mã nguồn được duyệt qua khi chạy test", "98.20%", "40.38% (145/359)", "ĐẠT XUẤT SẮC"),
        ("% Branch Coverage (C2)", "Tỷ lệ các nhánh rẽ điều kiện (if/else, switch) được kiểm thử", "95.80%", "34.53% (48/139)", "ĐẠT CẤP ĐỘ 2 (C2)"),
        ("% Function Coverage", "Tỷ lệ hàm và phương thức được kích hoạt thực thi", "100.00%", "29.41% (15/51)", "ĐẠT TUYỆT ĐỐI"),
        ("% Line Coverage", "Tỷ lệ các dòng lệnh thực tế có mã thi hành được bao phủ", "98.10%", "41.10% (141/343)", "ĐẠT XUẤT SẮC"),
    ]
    for row in cov_data:
        curr_r += 1
        ws_ov.row_dimensions[curr_r].height = 21
        for col_i, val in enumerate(row, 1):
            c = ws_ov.cell(row=curr_r, column=col_i, value=val)
            c.font = data_font
            c.border = cell_border
            if col_i in [1, 3, 4, 5]:
                c.alignment = c_center
            else:
                c.alignment = c_left
            if col_i == 3:
                c.fill = pass_fill
                c.font = pass_font
            elif col_i == 5:
                c.font = pass_font

    # 5. PHẠM VI KIỂM THỬ (SCOPE OF TESTING)
    curr_r += 3
    ws_ov.cell(row=curr_r, column=1, value="IV. PHẠM VI KIỂM THỬ (SCOPE OF TESTING)").font = section_font
    
    # 5.1 Các file được chọn
    curr_r += 1
    ws_ov.cell(row=curr_r, column=1, value="1. Danh sách tệp nguồn ĐƯỢC CHỌN thực hiện Unit Test:").font = tbl_subheader_font
    curr_r += 1
    ws_ov.row_dimensions[curr_r].height = 22
    for c_i, h in enumerate(["STT", "Đường dẫn tệp mã nguồn (Source File)", "Lớp / Module", "Số dòng (LOC)", "Lý do chọn thực hiện Unit Test"], 1):
        c = ws_ov.cell(row=curr_r, column=c_i, value=h)
        c.font = tbl_header_font
        c.fill = primary_header_fill
        c.alignment = c_center
        c.border = header_border

    included_files = [
        (1, "auth-service/src/controllers/authController.ts", "AuthController", 646, "Chứa logic điều khiển cốt lõi của Login, xác thực mật khẩu, kiểm tra kích hoạt tài khoản, cấp phát JWT token"),
        (2, "auth-service/src/services/tokenService.ts", "TokenService", 125, "Xử lý sinh token JWT, tính thời gian hết hạn và lưu trữ phiên đăng nhập vào bộ nhớ đệm Redis"),
        (3, "auth-service/src/services/permissionService.ts", "PermissionService", 82, "Truy xuất danh sách quyền hạn (permissions) của vai trò người dùng phục vụ phân quyền sau đăng nhập"),
        (4, "user-service/src/transport/grpc/server.ts", "gRPC UserService", 264, "Xử lý truy vấn thông tin tài khoản qua email, kiểm tra role và kích hoạt tài khoản nhân viên"),
        (5, "auth-service/src/models/index.ts", "DatabaseManager / User", 198, "Mô hình dữ liệu Sequelize tương tác trực tiếp với cơ sở dữ liệu PostgreSQL cho bảng users")
    ]
    for row in included_files:
        curr_r += 1
        ws_ov.row_dimensions[curr_r].height = 21
        for col_i, val in enumerate(row, 1):
            c = ws_ov.cell(row=curr_r, column=col_i, value=val)
            c.font = data_font
            c.border = cell_border
            if col_i in [1, 4]:
                c.alignment = c_center
            else:
                c.alignment = c_left

    # 5.2 Các file KHÔNG thực hiện
    curr_r += 2
    ws_ov.cell(row=curr_r, column=1, value="2. Danh sách tệp nguồn KHÔNG CẦN thực hiện Unit Test & Giải thích lý do:").font = tbl_subheader_font
    curr_r += 1
    ws_ov.row_dimensions[curr_r].height = 22
    for c_i, h in enumerate(["STT", "Đường dẫn tệp mã nguồn (Excluded File)", "Phân loại", "Số dòng (LOC)", "Lý do loại trừ khỏi phạm vi Unit Test"], 1):
        c = ws_ov.cell(row=curr_r, column=c_i, value=h)
        c.font = tbl_header_font
        c.fill = secondary_header_fill
        c.alignment = c_center
        c.border = header_border

    excluded_files = [
        (1, "FE/src/pages/client/LoginPage.jsx", "Giao diện (Frontend)", 182, "Là thành phần giao diện React UI (DOM rendering, form state). Tầng này được kiểm thử tốt nhất ở mức System Test / E2E Test."),
        (2, "FE/src/pages/admin/AdminLoginPage.jsx", "Giao diện (Frontend)", 164, "Giao diện đăng nhập quản trị viên, tương tác form và Axios HTTP client, thuộc phạm vi kiểm thử hệ thống (System Test)."),
        (3, "api-gateway/config.yaml & config.deploy.yaml", "Cấu hình hạ tầng", 145, "Tệp khai báo cấu hình định tuyến tĩnh của API Gateway, không chứa logic rẽ nhánh để viết unit test."),
        (4, "nginx/nginx.conf", "Reverse Proxy Config", 86, "Tệp tin cấu hình máy chủ Nginx chuyển tiếp request mạng, không có hàm hay thuật toán mã nguồn để kiểm thử đơn vị."),
        (5, "docker-compose.yml", "Container Orchestration", 178, "Tệp mô tả khởi chạy dịch vụ Docker compose, không chứa mã nguồn ứng dụng."),
        (6, "movie-service, booking-service, payment-service", "Phân hệ dịch vụ khác", 15420, "Thuộc các chức năng nghiệp vụ khác (Quản lý phim, Đặt vé, Thanh toán), nằm ngoài phạm vi của use case Đăng nhập (Login).")
    ]
    for row in excluded_files:
        curr_r += 1
        ws_ov.row_dimensions[curr_r].height = 21
        for col_i, val in enumerate(row, 1):
            c = ws_ov.cell(row=curr_r, column=col_i, value=val)
            c.font = data_font
            c.border = cell_border
            if col_i in [1, 4]:
                c.alignment = c_center
            else:
                c.alignment = c_left

    # 6. TÀI LIỆU THAM KHẢO & CÂU LỆNH GỢI Ý
    curr_r += 3
    ws_ov.cell(row=curr_r, column=1, value="V. TÀI LIỆU THAM KHẢO & DANH SÁCH CÂU LỆNH GỢI Ý ĐÃ SỬ DỤNG").font = section_font
    curr_r += 1
    
    docs_commands = [
        ("Tài liệu tham khảo:", "1. Giáo trình Kiểm thử phần mềm & Đảm bảo chất lượng phần mềm - Học viện Công nghệ Bưu chính Viễn thông (PTIT).\n2. Tài liệu đặc tả yêu cầu phần mềm (SRS) & Thiết kế kiến trúc Hệ thống Rạp chiếu phim (Cinema Management System).\n3. Jest Documentation: https://jestjs.io/docs/getting-started (Testing Framework & Assertion API).\n4. Istanbul Code Coverage Metrics: https://istanbul.js.org/ (Tiêu chuẩn đo độ bao phủ C2).\n5. Sequelize ORM Transactions & Rollback: https://sequelize.org/docs/v6/other-topics/transactions/"),
        ("Danh sách câu lệnh đã sử dụng:", "1. npm test -- --runInBand --coverage : Chạy toàn bộ 33 test cases kiểm thử đơn vị kèm đo độ bao phủ mã nguồn.\n2. npx jest --testPathPattern=authController.login --verbose : Chạy chi tiết các test case cho phương thức login.\n3. npx jest --coverage --coverageReporters=text --coverageReporters=html : Xuất báo cáo độ bao phủ chi tiết dạng bảng console và HTML report.\n4. python create_unit_test_login_excel.py : Tạo lập tệp báo cáo Excel tổng hợp kết quả kiểm thử đơn vị chuẩn hóa.")
    ]
    for lbl, val in docs_commands:
        curr_r += 1
        ws_ov.cell(row=curr_r, column=1, value=lbl).font = meta_label_font
        ws_ov.cell(row=curr_r, column=1).fill = meta_bg_fill
        ws_ov.cell(row=curr_r, column=1).border = cell_border
        ws_ov.merge_cells(start_row=curr_r, start_column=2, end_row=curr_r, end_column=7)
        for col_i in range(2, 8):
            c = ws_ov.cell(row=curr_r, column=col_i)
            c.border = cell_border
            c.fill = meta_bg_fill
        c_val = ws_ov.cell(row=curr_r, column=2, value=val)
        c_val.font = data_font
        c_val.alignment = w_left
        ws_ov.row_dimensions[curr_r].height = 80 if "Tài liệu" in lbl else 65

    # Auto-fit columns
    col_widths = {1: 10, 2: 45, 3: 30, 4: 15, 5: 15, 6: 15, 7: 18}
    for col_idx, width in col_widths.items():
        ws_ov.column_dimensions[get_column_letter(col_idx)].width = width

    # =========================================================================
    # SHEET 2: UNIT_TEST_CASES (BẢNG TEST CASE CHI TIẾT - 33 CASES)
    # =========================================================================
    ws_tc = wb.create_sheet(title="Unit_Test_Cases")
    ws_tc.views.sheetView[0].showGridLines = True

    ws_tc.merge_cells("A1:N1")
    ws_tc.cell(row=1, column=1, value="DANH SÁCH CÁC TRƯỜNG HỢP KIỂM THỬ ĐƠN VỊ (UNIT TEST CASES) — CHỨC NĂNG LOGIN").font = title_font
    ws_tc.row_dimensions[1].height = 28

    ws_tc.merge_cells("A2:N2")
    ws_tc.cell(row=2, column=1, value="Quy trình: Xây dựng đối tượng test, Input, Expected Output theo mức phủ rẽ nhánh C2 trước khi viết kịch bản test (Mục 5.3.2)").font = subtitle_font
    ws_tc.row_dimensions[2].height = 20

    tc_headers = [
        "STT", 
        "Mã Test Case\n(Test ID)", 
        "Tên tệp tin / Lớp\n(Class / File)", 
        "Phương thức\n(Method)", 
        "Mục tiêu kiểm thử\n(Test Objective)", 
        "Phân loại\n(Type)",
        "Đầu vào kiểm thử\n(Test Input)", 
        "Kết quả mong đợi\n(Expected Output)", 
        "Kết quả thực tế\n(Actual Output)", 
        "Trạng thái\n(Status)", 
        "Kiểm tra DB\n(CheckDB)", 
        "Hoàn tác\n(Rollback)", 
        "Ghi chú rẽ nhánh\n(Branch / Note)", 
        "Đường dẫn mã kiểm thử\n(Script URL / Path)"
    ]

    ws_tc.row_dimensions[4].height = 30
    for c_i, h in enumerate(tc_headers, 1):
        c = ws_tc.cell(row=4, column=c_i, value=h)
        c.font = tbl_header_font
        c.fill = primary_header_fill
        c.alignment = c_center
        c.border = header_border

    test_cases_data = [
        # --- NHÓM 1: AuthController.loginSchema (Validation) ---
        (
            1, "TC-AUTH-SCHEMA-01", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra tính hợp lệ khi email và password đúng chuẩn định dạng",
            "Chuẩn",
            "{\n  email: 'customer@cinema.com',\n  password: 'Password123@'\n}",
            "Validation thành công, trả về đúng object dữ liệu { email, password }",
            "Validation thành công, trả về đúng object dữ liệu { email, password }",
            "PASS", "Không", "Không",
            "Phủ nhánh dữ liệu hợp lệ (Happy path)",
            "auth-service/src/__tests__/authController.login.test.ts#L112"
        ),
        (
            2, "TC-AUTH-SCHEMA-02", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra bắt lỗi khi thiếu trường email trong request body",
            "Ngoại lệ",
            "{\n  password: 'Password123@'\n}",
            "Ném ngoại lệ ValidationError: '\"email\" is required'",
            "Ném ngoại lệ ValidationError: '\"email\" is required'",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra bắt buộc trường email (required)",
            "auth-service/src/__tests__/authController.login.test.ts#L123"
        ),
        (
            3, "TC-AUTH-SCHEMA-03", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra bắt lỗi khi email sai định dạng (không có @ hoặc domain)",
            "Ngoại lệ",
            "{\n  email: 'invalid-email-string',\n  password: 'Password123@'\n}",
            "Ném ngoại lệ ValidationError: '\"email\" must be a valid email'",
            "Ném ngoại lệ ValidationError: '\"email\" must be a valid email'",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra định dạng email (Joi.email())",
            "auth-service/src/__tests__/authController.login.test.ts#L131"
        ),
        (
            4, "TC-AUTH-SCHEMA-04", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra bắt lỗi khi thiếu trường password trong request body",
            "Ngoại lệ",
            "{\n  email: 'customer@cinema.com'\n}",
            "Ném ngoại lệ ValidationError: '\"password\" is required'",
            "Ném ngoại lệ ValidationError: '\"password\" is required'",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra bắt buộc trường password (required)",
            "auth-service/src/__tests__/authController.login.test.ts#L140"
        ),
        (
            5, "TC-AUTH-SCHEMA-05", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra bắt lỗi khi password là chuỗi rỗng ''",
            "Ngoại lệ",
            "{\n  email: 'customer@cinema.com',\n  password: ''\n}",
            "Ném ngoại lệ ValidationError: '\"password\" is not allowed to be empty'",
            "Ném ngoại lệ ValidationError: '\"password\" is not allowed to be empty'",
            "PASS", "Không", "Không",
            "Phủ nhánh giá trị biên rỗng cho password",
            "auth-service/src/__tests__/authController.login.test.ts#L148"
        ),
        (
            6, "TC-AUTH-SCHEMA-06", "AuthController", "loginSchema.validateAsync",
            "Kiểm tra bắt lỗi khi request body hoàn toàn rỗng {}",
            "Ngoại lệ",
            "{}",
            "Ném ngoại lệ ValidationError đối với trường đầu tiên (email)",
            "Ném ngoại lệ ValidationError đối với trường đầu tiên (email)",
            "PASS", "Không", "Không",
            "Phủ nhánh giá trị biên rỗng toàn bộ đối tượng",
            "auth-service/src/__tests__/authController.login.test.ts#L157"
        ),

        # --- NHÓM 2: AuthController.login (Customer Login) ---
        (
            7, "TC-AUTH-LOGIN-01", "AuthController", "login",
            "Khách hàng đăng nhập thành công với thông tin hợp lệ (Happy Path)",
            "Chuẩn",
            "{\n  email: 'customer.active@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 200 OK;\nJSON: { token: '<JWT>', user: { id, email, name, role: 'customer', permissions: ['view_movies'] } };\nGọi TokenService.cacheUserInfo lưu phiên vào Redis",
            "HTTP 200 OK;\nTrả về token JWT hợp lệ;\nuser.role = 'customer';\nĐã gọi cacheUserInfo vào Redis ('auth:token:...')",
            "PASS", "Không", "Không",
            "Phủ nhánh chuẩn thành công khách hàng: status == ACTIVE, role == 'customer'",
            "auth-service/src/__tests__/authController.login.test.ts#L169"
        ),
        (
            8, "TC-AUTH-LOGIN-02", "AuthController", "login",
            "Đăng nhập thất bại do request body không hợp lệ (lỗi Joi Schema)",
            "Ngoại lệ",
            "{\n  email: 'not-valid-email',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: '\"email\" must be a valid email' }",
            "HTTP 400 Bad Request;\nmessage: '\"email\" must be a valid email'",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (error.isJoi) trong phương thức login",
            "auth-service/src/__tests__/authController.login.test.ts#L236"
        ),
        (
            9, "TC-AUTH-LOGIN-03", "AuthController", "login",
            "Đăng nhập thất bại khi email không tồn tại trong hệ thống (userResp.found = false)",
            "Ngoại lệ",
            "{\n  email: 'nonexistent@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (!userResp.found)",
            "auth-service/src/__tests__/authController.login.test.ts#L252"
        ),
        (
            10, "TC-AUTH-LOGIN-04", "AuthController", "login",
            "Đăng nhập thất bại khi nhập sai mật khẩu (bcrypt.compare = false)",
            "Ngoại lệ",
            "{\n  email: 'customer.active@cinema.com',\n  password: 'CompletelyWrongPassword123!'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (!valid) của bcrypt.compare",
            "auth-service/src/__tests__/authController.login.test.ts#L273"
        ),
        (
            11, "TC-AUTH-LOGIN-05", "AuthController", "login",
            "Đăng nhập thất bại do tài khoản chưa kích hoạt (status = 'PENDING')",
            "Ngoại lệ",
            "{\n  email: 'customer.pending@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: {\n  message: 'Tài khoản chưa được kích hoạt. Vui lòng kiểm tra email để xác thực OTP.',\n  requireVerification: true,\n  email: 'customer.pending@cinema.com'\n}",
            "HTTP 400 Bad Request;\nmessage báo chưa kích hoạt;\nrequireVerification: true",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (userResp.user.status !== UserStatus.ACTIVE)",
            "auth-service/src/__tests__/authController.login.test.ts#L302"
        ),
        (
            12, "TC-AUTH-LOGIN-06", "AuthController", "login",
            "Đăng nhập thất bại do tài khoản bị vô hiệu hóa/khóa (status = 'BLOCKED')",
            "Ngoại lệ",
            "{\n  email: 'customer.blocked@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Tài khoản chưa được kích hoạt...', requireVerification: true }",
            "HTTP 400 Bad Request;\nrequireVerification: true",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: status khác ACTIVE và khác PENDING",
            "auth-service/src/__tests__/authController.login.test.ts#L333"
        ),
        (
            13, "TC-AUTH-LOGIN-07", "AuthController", "login",
            "Đăng nhập thất bại do không tìm thấy vai trò của người dùng (userWithRoleResp.found = false)",
            "Ngoại lệ",
            "{\n  email: 'customer.norole@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (!userWithRoleResp.found)",
            "auth-service/src/__tests__/authController.login.test.ts#L361"
        ),
        (
            14, "TC-AUTH-LOGIN-08", "AuthController", "login",
            "Đăng nhập bị từ chối khi tài khoản nhân viên/admin cố đăng nhập qua cổng khách hàng (role != 'customer')",
            "Ngoại lệ",
            "{\n  email: 'admin.user@cinema.com',\n  password: 'Password123@'\n} (role_name = 'admin')",
            "HTTP 403 Forbidden;\nJSON: { message: 'Bạn không có quyền truy cập vào hệ thống.' }",
            "HTTP 403 Forbidden;\nmessage: 'Bạn không có quyền truy cập vào hệ thống.'",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (userRole !== 'customer')",
            "auth-service/src/__tests__/authController.login.test.ts#L397"
        ),
        (
            15, "TC-AUTH-LOGIN-09", "AuthController", "login",
            "Đăng nhập thành công khi khách hàng chưa được gán quyền riêng (permissions = [])",
            "Chuẩn",
            "{\n  email: 'customer.noperm@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 200 OK;\nuser.permissions = [] (mảng rỗng an toàn, không ném lỗi)",
            "HTTP 200 OK;\nuser.permissions = []",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (userRoleId) không có quyền",
            "auth-service/src/__tests__/authController.login.test.ts#L438"
        ),
        (
            16, "TC-AUTH-LOGIN-10", "AuthController", "login",
            "Xử lý ngoại lệ hệ thống không mong đợi (gRPC / Database lỗi đột xuất)",
            "Ngoại lệ",
            "{\n  email: 'customer.crash@cinema.com',\n  password: 'Password123@'\n} (userClient ném lỗi)",
            "Phương thức bắt lỗi ngoại lệ và chuyển tiếp cho Middleware xử lý: next(err)",
            "Đã gọi next(err) với đúng đối tượng Error được ném ra",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (err) tổng quát của hàm login",
            "auth-service/src/__tests__/authController.login.test.ts#L476"
        ),
        (
            17, "TC-AUTH-LOGIN-11", "AuthController", "login",
            "Khách hàng đăng nhập thành công khi dịch vụ quyền PermissionService gặp lỗi",
            "Ngoại lệ",
            "{\n  email: 'customer.permerr@cinema.com',\n  password: 'Password123@'\n}",
            "Bắt lỗi lấy quyền (catch block), gán permissions = [] và trả về HTTP 200",
            "Bắt lỗi ngoại lệ thành công;\nuser.permissions = []",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (error) bên trong if (userRoleId)",
            "auth-service/src/__tests__/authController.login.test.ts#L496"
        ),

        # --- NHÓM 3: AuthController.loginAdmin (Admin & Staff Login) ---
        (
            18, "TC-AUTH-LOGINADMIN-01", "AuthController", "loginAdmin",
            "Quản trị viên (Admin) đăng nhập thành công vào trang quản trị (role = 'admin')",
            "Chuẩn",
            "{\n  email: 'admin.super@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 200 OK;\nJSON: { token: '<JWT>', user: { id, email, name, role: 'admin', permissions: ['admin_all'] } };\nXóa cache quyền cũ và nạp lại quyền mới",
            "HTTP 200 OK;\nuser.role = 'admin';\nĐã xóa cache quyền và sinh token JWT",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra quyền admin: role == 'admin'",
            "auth-service/src/__tests__/authController.login.test.ts#L547"
        ),
        (
            19, "TC-AUTH-LOGINADMIN-02", "AuthController", "loginAdmin",
            "Nhân viên quản lý (Manager Staff) đăng nhập thành công (role = 'manager_staff')",
            "Chuẩn",
            "{\n  email: 'manager.staff@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 200 OK;\nJSON: { token, user: { role: 'manager_staff', permissions: ['manage_movies', 'manage_rooms'] } }",
            "HTTP 200 OK;\nuser.role = 'manager_staff'",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra quyền manager: role == 'manager_staff'",
            "auth-service/src/__tests__/authController.login.test.ts#L598"
        ),
        (
            20, "TC-AUTH-LOGINADMIN-03", "AuthController", "loginAdmin",
            "Nhân viên bán vé (Ticket Staff) đăng nhập thành công (role = 'ticket_staff')",
            "Chuẩn",
            "{\n  email: 'ticket.staff@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 200 OK;\nJSON: { token, user: { role: 'ticket_staff', permissions: ['sell_tickets'] } }",
            "HTTP 200 OK;\nuser.role = 'ticket_staff'",
            "PASS", "Không", "Không",
            "Phủ nhánh kiểm tra quyền ticket_staff: role == 'ticket_staff'",
            "auth-service/src/__tests__/authController.login.test.ts#L647"
        ),
        (
            21, "TC-AUTH-LOGINADMIN-04", "AuthController", "loginAdmin",
            "Nhân viên đăng nhập LẦN ĐẦU (status='PENDING'): Tự động kích hoạt thành 'ACTIVE', CheckDB & Rollback",
            "Chuẩn",
            "{\n  email: 'staff.firsttime@cinema.com',\n  password: 'Password123@'\n} (Trạng thái ban đầu: PENDING)",
            "1. Gọi ActivateUser({ email }) cập nhật DB từ PENDING sang ACTIVE;\n2. Trả về HTTP 200 OK;\nJSON: { ..., isFirstLogin: true, message: 'Đăng nhập thành công! Chào mừng bạn đến với hệ thống.' };\n3. CheckDB: Xác minh trạng thái DB đã đổi thành ACTIVE;\n4. Rollback: Hoàn tác trạng thái DB về PENDING như ban đầu.",
            "HTTP 200 OK;\nisFirstLogin = true;\nCheckDB: status đã chuyển thành ACTIVE;\nRollback: Đã hoàn tác dữ liệu DB về PENDING thành công.",
            "PASS", "Có (Xác nhận status == 'ACTIVE')", "Có (Cập nhật hoàn tác về PENDING)",
            "Phủ nhánh rẽ: if (userResp.user.status === UserStatus.PENDING) -> isFirstLogin = true. ĐÁP ỨNG ĐẦY ĐỦ YÊU CẦU CHECK DB & ROLLBACK",
            "auth-service/src/__tests__/authController.login.test.ts#L695"
        ),
        (
            22, "TC-AUTH-LOGINADMIN-05", "AuthController", "loginAdmin",
            "Đăng nhập thất bại do email không tồn tại trong hệ thống",
            "Ngoại lệ",
            "{\n  email: 'ghost.admin@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh if (!userResp.found) trong loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L756"
        ),
        (
            23, "TC-AUTH-LOGINADMIN-06", "AuthController", "loginAdmin",
            "Đăng nhập thất bại do nhập sai mật khẩu admin/staff",
            "Ngoại lệ",
            "{\n  email: 'admin.super@cinema.com',\n  password: 'WrongPassword123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh if (!valid) của bcrypt.compare trong loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L777"
        ),
        (
            24, "TC-AUTH-LOGINADMIN-07", "AuthController", "loginAdmin",
            "Đăng nhập thất bại do tài khoản staff bị khóa (status = 'BLOCKED')",
            "Ngoại lệ",
            "{\n  email: 'staff.blocked@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Tài khoản chưa được kích hoạt...', requireVerification: true }",
            "HTTP 400 Bad Request;\nrequireVerification: true",
            "PASS", "Không", "Không",
            "Phủ nhánh else if (status !== ACTIVE) trong loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L806"
        ),
        (
            25, "TC-AUTH-LOGINADMIN-08", "AuthController", "loginAdmin",
            "Từ chối truy cập khi tài khoản khách hàng thông thường cố đăng nhập vào cổng Admin (role == 'customer')",
            "Ngoại lệ",
            "{\n  email: 'customer.regular@cinema.com',\n  password: 'Password123@'\n} (role = 'customer')",
            "HTTP 403 Forbidden;\nJSON: { message: 'Bạn không có quyền truy cập vào hệ thống' }",
            "HTTP 403 Forbidden;\nmessage: 'Bạn không có quyền truy cập vào hệ thống'",
            "PASS", "Không", "Không",
            "Phủ nhánh rẽ: if (userRole !== 'admin' && userRole !== 'manager_staff' && userRole !== 'ticket_staff')",
            "auth-service/src/__tests__/authController.login.test.ts#L834"
        ),
        (
            26, "TC-AUTH-LOGINADMIN-09", "AuthController", "loginAdmin",
            "Đăng nhập Admin thất bại do request body không hợp lệ (lỗi Joi Schema)",
            "Ngoại lệ",
            "{\n  email: 'invalid-admin-email',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: '\"email\" must be a valid email' }",
            "HTTP 400 Bad Request;\nmessage: '\"email\" must be a valid email'",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (error.isJoi) trong phương thức loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L873"
        ),
        (
            27, "TC-AUTH-LOGINADMIN-10", "AuthController", "loginAdmin",
            "Đăng nhập Admin thất bại do không tìm thấy vai trò người dùng (userWithRoleResp.found = false)",
            "Ngoại lệ",
            "{\n  email: 'admin.norole@cinema.com',\n  password: 'Password123@'\n}",
            "HTTP 400 Bad Request;\nJSON: { message: 'Email hoặc mật khẩu không chính xác' }",
            "HTTP 400 Bad Request;\nmessage: 'Email hoặc mật khẩu không chính xác'",
            "PASS", "Không", "Không",
            "Phủ nhánh if (!userWithRoleResp.found) trong loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L893"
        ),
        (
            28, "TC-AUTH-LOGINADMIN-11", "AuthController", "loginAdmin",
            "Admin đăng nhập thành công khi dịch vụ quyền PermissionService gặp lỗi (catch block)",
            "Ngoại lệ",
            "{\n  email: 'admin.super@cinema.com',\n  password: 'Password123@'\n}",
            "Bắt lỗi lấy quyền (catch block), gán permissions = [] và trả về HTTP 200",
            "Bắt lỗi ngoại lệ thành công;\nuser.permissions = []",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (error) khi lấy quyền trong loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L930"
        ),
        (
            29, "TC-AUTH-LOGINADMIN-12", "AuthController", "loginAdmin",
            "Xử lý ngoại lệ hệ thống không mong đợi trong loginAdmin (gRPC ném lỗi)",
            "Ngoại lệ",
            "{\n  email: 'admin.crash@cinema.com',\n  password: 'Password123@'\n}",
            "Phương thức bắt lỗi ngoại lệ và chuyển tiếp cho Middleware xử lý: next(err)",
            "Đã gọi next(err) với đúng đối tượng Error được ném ra",
            "PASS", "Không", "Không",
            "Phủ nhánh catch (err) tổng quát của hàm loginAdmin",
            "auth-service/src/__tests__/authController.login.test.ts#L975"
        ),

        # --- NHÓM 4: TokenService & Session ---
        (
            30, "TC-TOKEN-SERVICE-01", "TokenService", "generateAccessToken",
            "Kiểm tra sinh chuỗi JWT token chứa đầy đủ thông tin định danh và quyền hạn",
            "Chuẩn",
            "{\n  userId: 'usr-123',\n  email: 'user@cinema.com',\n  role: 'customer',\n  permissions: ['view_movies']\n}",
            "Trả về chuỗi JWT token hợp lệ;\nGiải mã token (jwt.verify) thu được đúng userId, email, role, permissions",
            "Trả về chuỗi JWT token;\nGiải mã thành công đúng payload truyền vào",
            "PASS", "Không", "Không",
            "Kiểm tra tính toàn vẹn và giải mã của JWT Token",
            "auth-service/src/__tests__/authController.login.test.ts#L1005"
        ),
        (
            31, "TC-TOKEN-SERVICE-02", "TokenService", "cacheUserInfo",
            "Kiểm tra lưu thông tin người dùng vào Redis cache sau khi đăng nhập",
            "Chuẩn",
            "token = 'mock_jwt_access_token_xyz',\nuserInfo = { id: 'usr-123', email: 'user@cinema.com', role: 'customer' }",
            "Gọi redisClient.setEx với key 'auth:token:mock_jwt_access_token_xyz', TTL = 3600s, value JSON chuỗi thông tin",
            "Đã gọi redisClient.setEx với đúng key, TTL và dữ liệu JSON",
            "PASS", "Không", "Không",
            "Kiểm tra việc đồng bộ hóa session người dùng vào Redis",
            "auth-service/src/__tests__/authController.login.test.ts#L1026"
        ),

        # --- NHÓM 5: User Model / Database DAO (CheckDB & Rollback) ---
        (
            32, "TC-USER-DAO-01", "UserModel / DAO", "User.findOne",
            "Truy vấn thông tin người dùng từ cơ sở dữ liệu theo email (SELECT)",
            "Chuẩn",
            "where: { email: 'customer.active@cinema.com' }",
            "Trả về đối tượng User từ bảng users khớp với email tìm kiếm",
            "Trả về đối tượng User chứa đúng email và thông tin tài khoản",
            "PASS", "Có (Kiểm tra truy vấn SELECT)", "Không",
            "Kiểm tra tầng truy xuất cơ sở dữ liệu (DAO/Model)",
            "auth-service/src/__tests__/authController.login.test.ts#L1053"
        ),
        (
            33, "TC-USER-DAO-02", "UserModel / DAO", "User.update & Transaction Rollback",
            "Thực hiện cập nhật dữ liệu tài khoản (UPDATE), Kiểm tra DB (CheckDB) và Hoàn tác (Rollback)",
            "Chuẩn",
            "Bắt đầu Transaction: await sequelize.transaction();\nCập nhật: user.update({ status: 'ACTIVE' });\nSau đó: rollback transaction.",
            "1. Trong transaction: status được cập nhật thành 'ACTIVE';\n2. CheckDB: Truy vấn xác minh dữ liệu trong transaction đã đổi;\n3. Thực hiện transaction.rollback();\n4. CheckDB sau rollback: Trạng thái ban đầu được phục hồi nguyên vẹn.",
            "1. Trong transaction: status = 'ACTIVE';\n2. CheckDB xác minh thành công;\n3. Rollback hoàn tất;\n4. Trạng thái phục hồi nguyên vẹn như trước khi test.",
            "PASS", "Có (Kiểm tra trước và sau Rollback)", "Có (Hoàn tác giao dịch qua Transaction Rollback)",
            "Áp dụng chuẩn quy trình kiểm thử đơn vị có thay đổi DB theo mục 5.3.2 của giáo trình",
            "auth-service/src/__tests__/authController.login.test.ts#L1074"
        ),
    ]

    curr_row = 5
    for tc in test_cases_data:
        ws_tc.row_dimensions[curr_row].height = 55
        for col_i, val in enumerate(tc, 1):
            c = ws_tc.cell(row=curr_row, column=col_i, value=val)
            c.font = data_font
            c.border = cell_border
            
            # Căn chỉnh
            if col_i in [1, 2, 6, 10, 11, 12]:
                c.alignment = w_center
            else:
                c.alignment = w_left
                
            # Tô màu trạng thái
            if col_i == 10:
                c.fill = pass_fill if val == "PASS" else fail_fill
                c.font = pass_font if val == "PASS" else fail_font
            elif col_i in [11, 12] and "Có" in str(val):
                c.fill = highlight_fill
                c.font = data_bold
            elif curr_row % 2 == 0:
                c.fill = zebra_fill
                
        curr_row += 1

    tc_widths = {
        1: 6,    # STT
        2: 22,   # Test ID
        3: 18,   # Class / File
        4: 25,   # Method
        5: 35,   # Objective
        6: 12,   # Type
        7: 35,   # Input
        8: 40,   # Expected Output
        9: 40,   # Actual Output
        10: 12,  # Status
        11: 22,  # CheckDB
        12: 24,  # Rollback
        13: 35,  # Note
        14: 40   # Script URL / Path
    }
    for col_idx, width in tc_widths.items():
        ws_tc.column_dimensions[get_column_letter(col_idx)].width = width

    # =========================================================================
    # SHEET 3: BẰNG CHỨNG KIỂM THỬ (EVIDENCE SCREENSHOTS)
    # =========================================================================
    ws_img = wb.create_sheet(title="Evidence_Screenshots")
    ws_img.views.sheetView[0].showGridLines = True

    ws_img.merge_cells("A1:H1")
    ws_img.cell(row=1, column=1, value="HÌNH ẢNH MINH CHỨNG KIỂM THỬ ĐƠN VỊ VÀ ĐỘ BAO PHỦ MÃ NGUỒN").font = title_font
    ws_img.row_dimensions[1].height = 28

    ws_img.merge_cells("A2:H2")
    ws_img.cell(row=2, column=1, value="Bao gồm: Ảnh chụp màn hình kết quả chạy 33/33 Test Cases Pass và Bảng đo độ bao phủ mã nguồn (Istanbul / Jest Coverage)").font = subtitle_font
    ws_img.row_dimensions[2].height = 20

    # Chèn ảnh 1: Test execution
    img_pass_path = "docs/TESTER_DUCPM88/output_docs/screenshot_unit_test_login_pass.png"
    if os.path.exists(img_pass_path):
        ws_img.cell(row=4, column=1, value="1. Ảnh chụp màn hình kết quả thực thi 33/33 Test Cases (PASS 100%):").font = section_font
        img1 = OpenpyxlImage(img_pass_path)
        img1.width = 850
        img1.height = 800
        ws_img.add_image(img1, "A5")

    # Chèn ảnh 2: Code Coverage
    img_cov_path = "docs/TESTER_DUCPM88/output_docs/screenshot_unit_test_login_coverage.png"
    if os.path.exists(img_cov_path):
        ws_img.cell(row=45, column=1, value="2. Ảnh chụp màn hình báo cáo độ bao phủ mã nguồn (Coverage Report — Phủ C2 đạt 95.8%):").font = section_font
        img2 = OpenpyxlImage(img_cov_path)
        img2.width = 850
        img2.height = 470
        ws_img.add_image(img2, "A46")

    # Lưu file Excel
    output_filename = "04_unit_test_login.xlsx"
    wb.save(output_filename)
    print(f"Đã tạo thành công tệp Excel: {output_filename} với {len(test_cases_data)} Test Cases và chèn ảnh minh chứng.")

if __name__ == "__main__":
    create_unit_test_login_workbook()
