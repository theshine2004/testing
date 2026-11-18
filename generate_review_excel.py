# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel():
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

    # Common styles
    font_family = "Calibri"
    title_font = Font(name=font_family, size=14, bold=True, color="1F4E79")
    subtitle_font = Font(name=font_family, size=11, bold=True, color="333333")
    meta_label_font = Font(name=font_family, size=10, bold=True, color="1F4E79")
    meta_val_font = Font(name=font_family, size=10, color="000000")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    data_font = Font(name=font_family, size=10, color="000000")
    data_bold = Font(name=font_family, size=10, bold=True, color="000000")
    pass_font = Font(name=font_family, size=10, bold=True, color="276A3C")
    fail_font = Font(name=font_family, size=10, bold=True, color="9C0006")
    na_font = Font(name=font_family, size=10, bold=True, color="808080")
    discussion_font = Font(name=font_family, size=10, italic=False, color="1F3864")

    # Fills
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    meta_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    na_fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    summary_total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    accent_bar_fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")

    # Borders
    thin_border_side = Side(border_style="thin", color="D9D9D9")
    dark_border_side = Side(border_style="thin", color="8EA9DB")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    table_border = Border(left=dark_border_side, right=dark_border_side, top=dark_border_side, bottom=dark_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=dark_border_side, bottom=dark_border_side)

    # Alignments
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    wrap_left_align = Alignment(horizontal="left", vertical="top", wrap_text=True)
    wrap_center_align = Alignment(horizontal="center", vertical="top", wrap_text=True)

    # -------------------------------------------------------------
    # 1. SHEET: J6_Dashboard
    # -------------------------------------------------------------
    ws_dash = wb.create_sheet(title="J6_Dashboard")
    ws_dash.views.sheetView[0].showGridLines = True

    ws_dash.cell(row=1, column=1, value="J6 CODE REVIEW SUMMARY DASHBOARD — BY FUNCTIONAL CLUSTER").font = title_font
    ws_dash.cell(row=2, column=1, value="Dự án: Xây dựng hệ thống quản lý rạp chiếu phim (Cinema Booking System)").font = subtitle_font
    ws_dash.cell(row=3, column=1, value="Repository: cinema-project-main (Golang Echo/Gin, NodeJS Express, ReactJS, PostgreSQL, Redis)").font = meta_label_font

    dash_headers = ["Cluster ID", "Tên phân hệ chức năng (Feature Cluster)", "Modules / Đường dẫn mã nguồn kiểm tra", "Pass", "Fail", "N/A", "Errors", "Kết luận đánh giá (Audit Conclusion)", "Tên Sheet chi tiết"]
    for col_idx, h_text in enumerate(dash_headers, 1):
        c = ws_dash.cell(row=5, column=col_idx, value=h_text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = center_align
        c.border = header_border
    ws_dash.row_dimensions[5].height = 28

    clusters_summary = [
        ("Cluster 1", "Login (Đăng nhập)", "FE: LoginPage.jsx, AdminLoginPage.jsx | Backend: auth-service/authController.ts", 14, 6, 0, 6, "Conditionally Approved", "J6_Login"),
        ("Cluster 2", "Registration (Đăng ký tài khoản)", "FE: RegisterPage.jsx, VerifyOtpPage.jsx | Backend: auth-service/authController.ts", 16, 4, 0, 4, "Conditionally Approved", "J6_Registration"),
        ("Cluster 3", "Edit Personal Information (Chỉnh sửa thông tin)", "FE: ProfilePage.jsx | Backend: user-service/userController.ts, userService.ts", 16, 4, 0, 4, "Conditionally Approved", "J6_EditProfile"),
        ("Cluster 4", "Room Management (Quản lý phòng chiếu)", "FE: RoomsPage.jsx, RoomFormPage.jsx | Backend: movie-service/room", 17, 3, 0, 3, "Conditionally Approved", "J6_RoomMgmt"),
        ("Cluster 5", "Seat Management (Quản lý ghế ngồi)", "FE: SeatsPage.jsx, SeatFormPage.jsx | Backend: movie-service/seat", 17, 3, 0, 3, "Conditionally Approved", "J6_SeatMgmt"),
        ("Cluster 6", "Online Booking (Đặt vé trực tuyến)", "FE: BookingPage.jsx, PaymentPage.jsx | Backend: booking-service/services/booking.go", 16, 4, 0, 4, "Conditionally Approved", "J6_OnlineBooking"),
        ("Cluster 7", "Box Office Booking (Bán vé tại quầy & Xuất vé)", "FE: BoxOfficePage.jsx, TicketSearchPage.jsx | Backend: booking-service", 17, 3, 0, 3, "Conditionally Approved", "J6_BoxOffice"),
        ("Cluster 8", "Staff & Permission (Quản lý nhân viên & Phân quyền)", "FE: StaffPage.jsx, PermissionManagementPage.jsx | Backend: user-service, auth-service", 17, 3, 0, 3, "Conditionally Approved", "J6_StaffPermission"),
        ("Cluster 9", "Revenue Analytics (Thống kê báo cáo doanh thu)", "FE: RevenueStatsPage.jsx, DashboardPage.jsx | Backend: analytics-service", 17, 3, 0, 3, "Conditionally Approved", "J6_RevenueAnalytics")
    ]

    total_pass = sum(x[3] for x in clusters_summary)
    total_fail = sum(x[4] for x in clusters_summary)
    total_na = sum(x[5] for x in clusters_summary)
    total_err = sum(x[6] for x in clusters_summary)

    for r_idx, row_data in enumerate(clusters_summary, 6):
        ws_dash.row_dimensions[r_idx].height = 24
        for c_idx, val in enumerate(row_data, 1):
            cell = ws_dash.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if c_idx in [1, 4, 5, 6, 7, 8, 9]:
                cell.alignment = center_align
            else:
                cell.alignment = left_align

            if c_idx == 4:
                cell.fill = pass_fill
                cell.font = pass_font
            elif c_idx == 5:
                cell.fill = fail_fill
                cell.font = fail_font
            elif c_idx == 8:
                cell.font = data_bold

    total_row_idx = 6 + len(clusters_summary)
    ws_dash.row_dimensions[total_row_idx].height = 26
    ws_dash.cell(row=total_row_idx, column=1, value="TOTAL").alignment = center_align
    ws_dash.cell(row=total_row_idx, column=2, value="Toàn bộ 9 phân hệ chức năng (All 9 Clusters)").alignment = left_align
    ws_dash.cell(row=total_row_idx, column=3, value="10 Microservices + React Client/Admin Portals").alignment = left_align
    ws_dash.cell(row=total_row_idx, column=4, value=total_pass).alignment = center_align
    ws_dash.cell(row=total_row_idx, column=5, value=total_fail).alignment = center_align
    ws_dash.cell(row=total_row_idx, column=6, value=total_na).alignment = center_align
    ws_dash.cell(row=total_row_idx, column=7, value=total_err).alignment = center_align
    ws_dash.cell(row=total_row_idx, column=8, value=f"Overall: 9 Conditionally Approved | 0 Rejected").alignment = center_align
    ws_dash.cell(row=total_row_idx, column=9, value="180 Questions Total").alignment = center_align

    for col in range(1, 10):
        c = ws_dash.cell(row=total_row_idx, column=col)
        c.font = data_bold
        c.fill = summary_total_fill
        c.border = Border(top=dark_border_side, bottom=Side(border_style="double", color="1F4E79"), left=thin_border_side, right=thin_border_side)

    # General notes on dashboard
    ws_dash.cell(row=total_row_idx + 2, column=1, value="GHI CHÚ VÀ ĐỊNH NGHĨA CHUNG CHO BẢNG KIỂM J6:").font = title_font
    dash_notes = [
        "1. Pass: Không phát hiện lỗi lập trình hoặc vi phạm chuẩn trong phạm vi câu hỏi.",
        "2. Fail: Phát hiện ít nhất 01 lỗi kỹ thuật, lỗi logic, lỗi bảo mật hoặc sai lệch giữa đặc tả luận văn và mã nguồn.",
        "3. N/A: Không áp dụng cho phân hệ này hoặc không khả dụng.",
        "4. Number of Errors: Tổng số lỗi cụ thể đã được định vị (kèm file và số dòng chính xác) được đếm trong phân hệ.",
        "5. Mọi câu hỏi ở Bảng J6 đã được loại bỏ các câu hỏi đặc thù của ngôn ngữ C (như phép toán con trỏ C) và bổ sung các câu hỏi kiểm tra Microservices, React Hooks, Redis Mutex, Joi validation, Transactional Outbox."
    ]
    for idx, n in enumerate(dash_notes, total_row_idx + 3):
        ws_dash.cell(row=idx, column=1, value=n).font = meta_val_font

    ws_dash.column_dimensions["A"].width = 14
    ws_dash.column_dimensions["B"].width = 30
    ws_dash.column_dimensions["C"].width = 50
    ws_dash.column_dimensions["D"].width = 10
    ws_dash.column_dimensions["E"].width = 10
    ws_dash.column_dimensions["F"].width = 10
    ws_dash.column_dimensions["G"].width = 10
    ws_dash.column_dimensions["H"].width = 28
    ws_dash.column_dimensions["I"].width = 22

    # -------------------------------------------------------------
    # Helper to create J6 functional checklist sheets
    # -------------------------------------------------------------
    def create_j6_sheet(sheet_name, cluster_num, cluster_name, module_path, questions, conclusion, discussion_lines):
        ws = wb.create_sheet(title=sheet_name)
        ws.views.sheetView[0].showGridLines = True

        pass_count = sum(1 for q in questions if q[1] == "Pass")
        fail_count = sum(1 for q in questions if q[1] == "Fail")
        na_count = sum(1 for q in questions if q[1] == "N/A")
        err_count = sum(q[3] for q in questions) # number of errors in question

        # Header block
        ws.cell(row=1, column=1, value="Project Name:").font = meta_label_font
        ws.cell(row=1, column=2, value="Xây dựng hệ thống quản lý rạp chiếu phim (Cinema Booking System)").font = meta_val_font

        ws.cell(row=2, column=1, value="Reviewed Document:").font = meta_label_font
        ws.cell(row=2, column=2, value=f"Repository: cinema-project-main ({module_path})").font = meta_val_font

        ws.cell(row=3, column=1, value="Reviewed Feature/Scope:").font = meta_label_font
        ws.cell(row=3, column=2, value=f"Cluster {cluster_num}: {cluster_name}").font = meta_val_font

        ws.cell(row=4, column=1, value="Number of Pass / Fail / N/A / Number of Errors:").font = meta_label_font
        ws.cell(row=4, column=2, value=f"Pass: {pass_count} | Fail: {fail_count} | N/A: {na_count} | Number of Errors: {err_count}").font = meta_val_font
        ws.cell(row=4, column=3, value=f"Total: {len(questions)} (Pass: {pass_count}, Fail: {fail_count}, N/A: {na_count})").font = meta_label_font
        ws.cell(row=4, column=4, value=f"Errors Counted: {err_count}").font = meta_label_font

        ws.cell(row=5, column=1, value="Quick Counters:").font = meta_label_font
        ws.cell(row=5, column=2, value=f"Pass: {pass_count}").font = pass_font
        ws.cell(row=5, column=3, value=f"Fail: {fail_count}").font = fail_font
        ws.cell(row=5, column=4, value=f"N/A: {na_count}").font = na_font

        # Style metadata block
        for r in range(1, 6):
            ws.row_dimensions[r].height = 20
            ws.cell(row=r, column=1).fill = meta_fill
            for c in range(1, 5):
                ws.cell(row=r, column=c).border = Border(bottom=Side(style="thin", color="E0E0E0"))

        # Table header
        headers = ["No.", "Checklist Question", "Review Result (Pass / Fail / N/A)", "Notes (for Fail, NA case please explain in detail, list all error you found)"]
        ws.row_dimensions[6].height = 26
        for c_idx, h_text in enumerate(headers, 1):
            cell = ws.cell(row=6, column=c_idx, value=h_text)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_align
            cell.border = header_border

        # Question rows
        curr_row = 7
        for q_idx, q_data in enumerate(questions, 1):
            q_text, q_res, q_notes, _ = q_data
            ws.row_dimensions[curr_row].height = 36 if len(q_notes) > 80 else 24

            c1 = ws.cell(row=curr_row, column=1, value=q_idx)
            c1.font = data_font
            c1.alignment = center_align
            c1.border = cell_border

            c2 = ws.cell(row=curr_row, column=2, value=q_text)
            c2.font = data_font
            c2.alignment = wrap_left_align
            c2.border = cell_border

            c3 = ws.cell(row=curr_row, column=3, value=q_res)
            c3.alignment = center_align
            c3.border = cell_border
            if q_res == "Pass":
                c3.font = pass_font
                c3.fill = pass_fill
            elif q_res == "Fail":
                c3.font = fail_font
                c3.fill = fail_fill
            else:
                c3.font = na_font
                c3.fill = na_fill

            c4 = ws.cell(row=curr_row, column=4, value=q_notes)
            c4.font = data_font
            c4.alignment = wrap_left_align
            c4.border = cell_border

            curr_row += 1

        # Conclusion and Discussion block
        curr_row += 1
        ws.row_dimensions[curr_row].height = 22
        ws.cell(row=curr_row, column=1, value="Conclusion:").font = meta_label_font
        ws.cell(row=curr_row, column=2, value=conclusion).font = data_bold

        curr_row += 1
        ws.row_dimensions[curr_row].height = 22
        ws.cell(row=curr_row, column=1, value="Discussion:").font = meta_label_font
        ws.cell(row=curr_row, column=2, value=discussion_lines[0]).font = discussion_font

        for d_line in discussion_lines[1:]:
            curr_row += 1
            ws.row_dimensions[curr_row].height = 20
            ws.cell(row=curr_row, column=2, value=d_line).font = discussion_font

        # Column widths
        ws.column_dimensions["A"].width = 8
        ws.column_dimensions["B"].width = 46
        ws.column_dimensions["C"].width = 18
        ws.column_dimensions["D"].width = 65

    # -------------------------------------------------------------
    # 20 Standard J6 Questions Template generator helper
    # -------------------------------------------------------------
    base_q_texts = [
        "1. Quy chuẩn lập trình: Mã nguồn có tuân thủ quy chuẩn Clean Code, tiêu chuẩn định dạng và kiến trúc quy định không?",
        "2. Chú thích nội dòng: Các hàm, module nghiệp vụ phức tạp có được viết chú thích (JSDoc, Go doc comments) đầy đủ không?",
        "3. Quy ước đặt tên: Tên biến, hàm, hằng số, struct/interface có tuân thủ đúng quy ước (camelCase / PascalCase) không?",
        "4. Định dạng mã nguồn: Mã nguồn có được thụt lề, định dạng chuẩn (gofmt, Prettier, ESLint) thống nhất không?",
        "5. Tái sử dụng hàm chung: Các logic dùng chung có được tách thành helper/service chung, tránh duplicate code (DRY) không?",
        "6. Mã nguồn dư thừa/rác: Có tồn tại mã nguồn rác, biến không dùng, đoạn code tính năng bỏ dở (dead UI / dummy code) không?",
        "7. An toàn con trỏ/giá trị rỗng: Các con trỏ (Go *T) và biến nullable (null, undefined trong JS) có được kiểm tra an toàn không?",
        "8. Giới hạn chỉ mục mảng/slice: Các thao tác truy cập phần tử qua index [i] có được kiểm tra độ dài tránh Out of Bounds không?",
        "9. Khởi tạo mảng/đối tượng: Các slice, map, mảng, state React có được khởi tạo đúng kiểu và giá trị mặc định ban đầu không?",
        "10. Điều kiện rẽ nhánh: Các biểu thức điều kiện trong if/else, switch/case có chính xác, vét cạn và xử lý đầy đủ các nhánh ngoại lệ không?",
        "11. Điều kiện dừng vòng lặp: Mọi vòng lặp (for, while) có điều kiện dừng rõ ràng và khả thi, không có nguy cơ lặp vô tận không?",
        "12. Kiểm tra chia cho 0: Trong các phép tính chia (tính tỷ lệ, tiền tệ, phân trang), mẫu số có được kiểm tra != 0 trước khi chia không?",
        "13. Tối ưu câu lệnh trong vòng lặp: Có câu lệnh truy vấn database, gọi RPC, hoặc xử lý nặng nào đặt trong vòng lặp (lỗi N+1) không?",
        "14. Độ sâu lồng câu lệnh if: Các câu lệnh if có bị lồng nhau quá 3 tầng (nested ifs > 3 levels) gây khó bảo trì không?",
        "15. Khớp tham số giao diện: Tham số thực tế truyền vào hàm / API endpoint / gRPC Protobuf có khớp hoàn toàn với đặc tả không?",
        "16. Biến không sử dụng: Có biến nào được khai báo nhưng không bao giờ được đọc hoặc sử dụng trong hàm không?",
        "17. Tối ưu truy vấn & chỉ mục CSDL: Các câu lệnh truy vấn CSDL có tận dụng index (Primary/Foreign Key) và tránh full table scan không?",
        "18. Kiểm tra trạng thái lỗi: Sau mỗi lần thực thi câu lệnh SQL / gọi API bên ngoài / gọi gRPC, trạng thái lỗi có được kiểm tra triệt để không?",
        "19. Kiểm soát đồng thời & Khóa dữ liệu: Các nghiệp vụ cập nhật tài nguyên dùng chung có cơ chế khóa (Redis lock, DB lock) chống race condition không?",
        "20. Thông điệp lỗi & Bảo mật thông tin: Các thông báo lỗi trả về có rõ ràng, được Việt hóa và không để lộ thông tin nhạy cảm không?"
    ]

    # -------------------------------------------------------------
    # CLUSTER 1: LOGIN
    # -------------------------------------------------------------
    q_login = [
        (base_q_texts[0], "Pass", "Tuân thủ kiến trúc phân tầng Controller - Service - gRPC Client và component React chuẩn.", 0),
        (base_q_texts[1], "Pass", "Có chú thích rõ ràng các hàm xác thực và middleware gRPC.", 0),
        (base_q_texts[2], "Pass", "Đặt tên hàm, biến chuẩn camelCase (Node.js) và PascalCase (React components).", 0),
        (base_q_texts[3], "Pass", "Định dạng thống nhất với Prettier và ESLint.", 0),
        (base_q_texts[4], "Pass", "Sử dụng TokenService và PermissionService tập trung, tái sử dụng tốt.", 0),
        (base_q_texts[5], "Fail", "FE/LoginPage.jsx: dòng 13, 107-111 khai báo state 'remember' nhưng handleSubmit không dùng; dòng 113-118 nút 'Quên mật khẩu?' là thẻ button rỗng không có onClick hay navigation (Dead UI).", 2),
        (base_q_texts[6], "Pass", "authController.ts kiểm tra null/undefined của req.body và userResp an toàn.", 0),
        (base_q_texts[7], "Pass", "Không có thao tác index mảng nguy hiểm; mảng permissions được map qua hàm có sẵn.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo state React (email, password, error, showPassword) đầy đủ giá trị mặc định.", 0),
        (base_q_texts[9], "Fail", "auth-service/src/controllers/authController.ts lines 252-259: if (userResp.user.status !== UserStatus.ACTIVE) gộp chung mọi status không phải ACTIVE (kể cả SUSPENDED/INACTIVE) đều bắt verify OTP qua email (sai lệch logic phân loại trạng thái người dùng).", 1),
        (base_q_texts[10], "Pass", "Các hàm xác thực xử lý tuần tự theo Promise/async-await, không sử dụng vòng lặp vô hạn.", 0),
        (base_q_texts[11], "N/A", "Chức năng đăng nhập không thực hiện phép toán số học chia.", 0),
        (base_q_texts[12], "Pass", "Không có câu lệnh query hoặc gọi RPC trong vòng lặp.", 0),
        (base_q_texts[13], "Pass", "Độ sâu lồng if tối đa 2 cấp nhờ sử dụng return early pattern.", 0),
        (base_q_texts[14], "Fail", "Lệch đặc tả Luận văn Bảng 1 trang 30: Đặc tả quy định Đăng nhập dùng chung cho cả 4 Actor (Khách hàng, Nhân viên, Quản trị) về trang Home. Thực tế code chia 2 cổng: Khách hàng ở /login, Nhân viên ở /admin/login. Nếu Admin đăng nhập tại /login bị chặn lỗi 403 Forbidden.", 1),
        (base_q_texts[15], "Pass", "Đã dọn dẹp các biến cục bộ, không có biến thừa trong authController.ts.", 0),
        (base_q_texts[16], "Pass", "Truy vấn GetUserByEmail tận dụng index unique trên cột email của bảng tblUser.", 0),
        (base_q_texts[17], "Pass", "Kiểm tra kỹ err từ gRPC call userClient.GetUserByEmail và userClient.GetUserWithRoleByEmail.", 0),
        (base_q_texts[18], "Fail", "auth-service/src/controllers/authController.ts: Endpoint /auth/login không có cơ chế Rate Limiting / Account Lockout sau 5 lần nhập sai mật khẩu liên tiếp (nguy cơ Brute-force mật khẩu).", 1),
        (base_q_texts[19], "Fail", "authController.ts lines 328-330: Khi form để trống hoặc sai kiểu, Joi trả về lỗi tiếng Anh thô ('\"email\" is required') thay vì thông báo tiếng Việt theo chuẩn đặc tả ('Vui lòng điền đầy đủ thông tin').", 1)
    ]
    disc_login = [
        "1. Điểm mạnh: Kiến trúc xác thực JWT tích hợp Redis cache thông tin người dùng và phân quyền RBAC phân tán qua gRPC hoạt động ổn định, độ trễ thấp.",
        "2. Vấn đề phát hiện: Checkbox 'Ghi nhớ đăng nhập' và nút 'Quên mật khẩu' trên giao diện chưa được lập trình chức năng thực tế (Dead UI). Lỗi logic nghiêm trọng khi tài khoản bị khóa (SUSPENDED) lại bị hệ thống thông báo là chưa xác thực OTP.",
        "3. Rủi ro lớn: Thiếu cơ chế giới hạn số lần thử mật khẩu (Brute-force lockout) tại auth-service; Xung đột giữa tài liệu đặc tả (luận văn mô tả 1 cổng đăng nhập chung) và mã nguồn (tách biệt 2 cổng client và admin)."
    ]
    create_j6_sheet("J6_Login", 1, "Login (Đăng nhập)", "FE/src/pages/client/LoginPage.jsx, AdminLoginPage.jsx, auth-service/authController.ts", q_login, "Conditionally Approved (Cần sửa lỗi trạng thái và cập nhật tài liệu)", disc_login)

    # -------------------------------------------------------------
    # CLUSTER 2: REGISTRATION
    # -------------------------------------------------------------
    q_reg = [
        (base_q_texts[0], "Pass", "Mã nguồn frontend và backend tuân thủ tốt kiến trúc async/await và validation qua Joi schema.", 0),
        (base_q_texts[1], "Pass", "Code có chú thích các bước gửi mã OTP qua Redis Pub/Sub và tạo user pending.", 0),
        (base_q_texts[2], "Pass", "Quy ước đặt tên biến nhất quán giữa form và API (email, password, firstName, lastName).", 0),
        (base_q_texts[3], "Pass", "Cấu trúc form đăng ký đẹp mắt, responsive tốt với Tailwind CSS.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng hàm generateOTP() và saveOTPToCache() dùng chung trong authController.", 0),
        (base_q_texts[5], "Pass", "Không phát hiện mã nguồn chết trong RegisterPage.jsx và VerifyOtpPage.jsx.", 0),
        (base_q_texts[6], "Pass", "Kiểm tra an toàn giá trị rỗng của address, firstName, lastName.", 0),
        (base_q_texts[7], "Pass", "Không có lỗi tràn mảng index.", 0),
        (base_q_texts[8], "Pass", "State form đăng ký khởi tạo đầy đủ các trường rỗng.", 0),
        (base_q_texts[9], "Fail", "authController.ts line 188: Khi email đã tồn tại, trả về BAD_REQUEST với ErrorMessages.EMAIL_EXISTS; tuy nhiên Luận văn Bảng 2 trang 31 lại ghi đặc tả exception là 'Tài khoản/mật khẩu không chính xác' (lỗi copy paste trong tài liệu luận văn).", 1),
        (base_q_texts[10], "Pass", "Luồng xử lý OTP có TTL 300 giây và tự động đếm max 5 lần thử.", 0),
        (base_q_texts[11], "N/A", "Không có phép chia trong đăng ký.", 0),
        (base_q_texts[12], "Pass", "Không có query trong loop.", 0),
        (base_q_texts[13], "Pass", "Các lệnh if phẳng, dễ theo dõi.", 0),
        (base_q_texts[14], "Fail", "RegisterPage.jsx có trường 'address' không bắt buộc, trong khi bảng đặc tả Luận văn Bảng 2 và Sơ đồ tuần tự Hình 20 trang 55 không mô tả trường địa chỉ trong payload đăng ký.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa khai báo.", 0),
        (base_q_texts[16], "Pass", "Kiểm tra trùng email qua gRPC GetUserByEmail có index unique trong DB.", 0),
        (base_q_texts[17], "Fail", "authController.ts lines 207-212: Sử dụng Redis Pub/Sub (redisPubSubClient.publish) để gửi sự kiện EMAIL_VERIFY; cơ chế này không bền vững (fire-and-forget), nếu worker gửi email bị sập thì thông điệp OTP bị mất vĩnh viễn, người dùng không nhận được email.", 1),
        (base_q_texts[18], "Pass", "Tất cả các lỗi gRPC call được kiểm tra và reject về catch block.", 0),
        (base_q_texts[19], "Fail", "FE/RegisterPage.jsx & authController.ts lines 153-160: Lỗi validation từ Joi trả về tiếng Anh ('\"confirmPassword\" must be [ref:password]') khi submit dữ liệu không khớp nếu vượt qua kiểm tra frontend.", 1)
    ]
    disc_reg = [
        "1. Điểm mạnh: Cơ chế sinh mã OTP 6 số ngẫu nhiên kèm bộ nhớ đệm Redis có TTL 300 giây và giới hạn 5 lần nhập sai giúp ngăn chặn brute-force OTP hiệu quả.",
        "2. Vấn đề phát hiện: Sử dụng Redis Pub/Sub thay vì Transactional Outbox khiến việc gửi email OTP có rủi ro mất mát thông điệp nếu service gặp sự cố. Bảng đặc tả 2 trong luận văn bị lỗi copy-paste ghi sai thông báo lỗi khi trùng email.",
        "3. Rủi ro lớn: Thiếu cơ chế kích hoạt lại email nếu Redis Pub/Sub thất bại; thông báo lỗi Joi chưa được Việt hóa toàn diện."
    ]
    create_j6_sheet("J6_Registration", 2, "Registration (Đăng ký tài khoản)", "FE/src/pages/client/RegisterPage.jsx, VerifyOtpPage.jsx, auth-service/src/controllers/authController.ts", q_reg, "Conditionally Approved", disc_reg)

    # -------------------------------------------------------------
    # CLUSTER 3: EDIT PERSONAL INFO
    # -------------------------------------------------------------
    q_profile = [
        (base_q_texts[0], "Pass", "Tuân thủ tốt mô hình MVC trong user-service và component React trong ProfilePage.jsx.", 0),
        (base_q_texts[1], "Pass", "Các hàm cập nhật user và kết nối ví Web3 có chú thích đầy đủ.", 0),
        (base_q_texts[2], "Pass", "Tên hàm, biến tuân thủ camelCase và cú pháp Ethers.js chuẩn.", 0),
        (base_q_texts[3], "Pass", "Code ProfilePage.jsx phân tách rõ ràng các state UI và state dữ liệu.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng userService.getUserById và userService.updateUser.", 0),
        (base_q_texts[5], "Fail", "FE/src/pages/client/ProfilePage.jsx lines 118-121: Số dư ví tiền điện tử BTC và USDT bị hardcode giả lập (BTC: '0.01', USDT: '1000') thay vì đọc từ mạng blockchain hoặc hợp đồng ERC-20.", 1),
        (base_q_texts[6], "Pass", "Kiểm tra window.ethereum an toàn trước khi gọi Ethers.js provider.", 0),
        (base_q_texts[7], "Pass", "Format địa chỉ ví kiểm tra độ dài chuỗi an toàn trước khi slice.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo editForm clone từ userData an toàn qua object spread.", 0),
        (base_q_texts[9], "Pass", "Các nhánh kiểm tra quyền cập nhật thông tin chính xác (chỉ cho phép sửa thông tin của chính mình hoặc admin).", 0),
        (base_q_texts[10], "Pass", "Không có vòng lặp tiềm ẩn nguy cơ lặp vô hạn.", 0),
        (base_q_texts[11], "N/A", "Không có phép toán chia trong module này.", 0),
        (base_q_texts[12], "Pass", "Không gọi query lặp trong vòng lặp.", 0),
        (base_q_texts[13], "Pass", "Các câu lệnh if không bị lồng quá 3 tầng.", 0),
        (base_q_texts[14], "Fail", "ProfilePage.jsx line 156: Bóc tách loại bỏ trường email ({ email, ...updateData }) trước khi gửi API cập nhật, trong khi Luận văn Bảng 19 không nói rõ việc cấm đổi email hay cơ chế xác thực khi thay đổi email.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa khai báo trong userController.ts.", 0),
        (base_q_texts[16], "Pass", "Truy vấn update theo Primary Key (id) của bảng tblUser có chỉ mục PK.", 0),
        (base_q_texts[17], "Fail", "user-service/src/controllers/userController.ts lines 81-100: Hàm updateUser chỉ bắt lỗi INVALID_REQUEST và USER_NOT_FOUND, nếu xảy ra lỗi DB kết nối hoặc lỗi trùng số điện thoại thì đẩy next(error) làm trả về lỗi 500 không có thông điệp rõ ràng.", 1),
        (base_q_texts[18], "Pass", "Có kiểm tra quyền xác thực qua AuthenticatedRequest middleware.", 0),
        (base_q_texts[19], "Fail", "ProfilePage.jsx lines 82, 95, 98, 108: Sử dụng hàm alert() nguyên thủy của trình duyệt thay vì Toast notification component, làm giảm trải nghiệm người dùng.", 1)
    ]
    disc_profile = [
        "1. Điểm mạnh: Tích hợp ví Web3 (MetaMask qua Ethers.js) mượt mà, lưu trữ địa chỉ ví on-chain vào customer profile; phân quyền chỉnh sửa chặt chẽ theo user_id.",
        "2. Vấn đề phát hiện: Hardcode số dư ví BTC và USDT; thông báo giao diện còn dùng alert() thô sơ; chưa có quy chuẩn nghiệp vụ rõ ràng trong luận văn về việc thay đổi email.",
        "3. Rủi ro lớn: Cần kiểm tra kỹ các ràng buộc số điện thoại để tránh lỗi Database 500 khi người dùng nhập số điện thoại đã tồn tại."
    ]
    create_j6_sheet("J6_EditProfile", 3, "Edit Personal Info (Chỉnh sửa thông tin)", "FE/src/pages/client/ProfilePage.jsx, user-service/src/controllers/userController.ts, userService.ts", q_profile, "Conditionally Approved", disc_profile)

    # -------------------------------------------------------------
    # CLUSTER 4: ROOM MANAGEMENT
    # -------------------------------------------------------------
    q_room = [
        (base_q_texts[0], "Pass", "movie-service viết bằng Golang tuân thủ Clean Architecture chuẩn (Entity, Repository, Business, REST Transport).", 0),
        (base_q_texts[1], "Pass", "Các hàm nghiệp vụ RoomBiz và Repository có interface và comment rõ ràng.", 0),
        (base_q_texts[2], "Pass", "Tuân thủ quy ước đặt tên chuẩn Go (PascalCase cho exported, camelCase cho internal).", 0),
        (base_q_texts[3], "Pass", "Định dạng code bằng gofmt chuẩn xác 100%.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng các package chung: caching, db, response, paging.", 0),
        (base_q_texts[5], "Pass", "Không có dead code trong module room.", 0),
        (base_q_texts[6], "Pass", "Kiểm tra updates == nil và room == nil an toàn trước khi truy xuất trường.", 0),
        (base_q_texts[7], "Pass", "Mảng phòng chiếu được phân trang qua Limit/Offset chuẩn xác.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo struct Room với UUID ngẫu nhiên và thời gian tạo hiện tại.", 0),
        (base_q_texts[9], "Fail", "movie-service/internal/module/room/business/business.go lines 187-199: Hàm DeleteRoom gọi trực tiếp repository.Delete mà KHÔNG kiểm tra xem phòng chiếu có đang chứa ghế (seats) hoặc suất chiếu (showtimes) hay không, dẫn đến lỗi Foreign Key Constraint 500 ở Database.", 1),
        (base_q_texts[10], "Pass", "Không có vòng lặp nguy hiểm trong xử lý phòng chiếu.", 0),
        (base_q_texts[11], "N/A", "Không có phép toán chia trong module phòng.", 0),
        (base_q_texts[12], "Pass", "Truy vấn phân trang sử dụng một câu query đếm và một câu query lấy dữ liệu riêng biệt, không có N+1.", 0),
        (base_q_texts[13], "Pass", "Các lệnh if phẳng, áp dụng guard clauses tốt.", 0),
        (base_q_texts[14], "Pass", "Interface parameters giữa REST handler và Business logic khớp chuẩn.", 0),
        (base_q_texts[15], "Pass", "Không có biến rác chưa dùng.", 0),
        (base_q_texts[16], "Pass", "Tìm kiếm phòng theo room_number và status tận dụng index trong PostgreSQL.", 0),
        (base_q_texts[17], "Pass", "Mọi câu lệnh repository đều kiểm tra if err != nil và bọc lỗi bằng fmt.Errorf.", 0),
        (base_q_texts[18], "Fail", "business.go lines 133, 182, 196: Hàm clearCacheForRoom chỉ xóa cache chi tiết phòng theo id mà không xóa cache của danh sách phân trang (keyRoomsList), có thể gây dữ liệu phân trang cũ (stale cache).", 1),
        (base_q_texts[19], "Fail", "transport/rest/api.go: Lỗi ErrRoomNumberExists trả về chuỗi tiếng Anh 'room number already exists', chưa đồng bộ thông điệp tiếng Việt 'Thêm phòng chiếu không thành công' theo Luận văn Bảng 5 trang 34.", 1)
    ]
    disc_room = [
        "1. Điểm mạnh: Cấu trúc Go Clean Architecture cực kỳ chuẩn mực, áp dụng dependency injection qua samber/do và caching Redis hiệu quả.",
        "2. Vấn đề phát hiện: Thiếu kiểm tra ràng buộc toàn vẹn khóa ngoại trước khi xóa phòng chiếu; cơ chế xóa cache danh sách phân trang chưa triệt để.",
        "3. Rủi ro lớn: Xóa phòng chiếu đang có lịch chiếu hoặc ghế ngồi sẽ làm sập giao dịch CSDL với lỗi 500 nếu không có try-catch ngoại lệ Foreign Key."
    ]
    create_j6_sheet("J6_RoomMgmt", 4, "Room Management (Quản lý phòng chiếu)", "movie-service/internal/module/room/business, repository, transport | FE/src/pages/admin/RoomsPage.jsx", q_room, "Conditionally Approved", disc_room)

    # -------------------------------------------------------------
    # CLUSTER 5: SEAT MANAGEMENT
    # -------------------------------------------------------------
    q_seat = [
        (base_q_texts[0], "Pass", "Mã nguồn Go module seat tuân thủ chặt chẽ Clean Architecture.", 0),
        (base_q_texts[1], "Pass", "Có tài liệu chú thích các loại ghế (REGULAR, VIP, COUPLE) và trạng thái ghế.", 0),
        (base_q_texts[2], "Pass", "Quy ước đặt tên chuẩn xác theo Go conventions.", 0),
        (base_q_texts[3], "Pass", "Định dạng code bằng gofmt đồng nhất.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng module caching và repository pattern.", 0),
        (base_q_texts[5], "Pass", "Không phát hiện mã nguồn chết.", 0),
        (base_q_texts[6], "Pass", "Kiểm tra nil cho con trỏ seat và updates an toàn.", 0),
        (base_q_texts[7], "Pass", "Kiểm tra danh sách ids rỗng an toàn trong GetSeatsByIds.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo struct Seat và map vị trí ghế chính xác.", 0),
        (base_q_texts[9], "Fail", "movie-service/internal/module/seat/business/business.go: Hàm DeleteSeat không kiểm tra trong bảng tickets xem ghế đã từng được mua hay chưa, có nguy cơ vi phạm ràng buộc dữ liệu vé đã bán.", 1),
        (base_q_texts[10], "Pass", "Vòng lặp duyệt danh sách ghế có điều kiện dừng rõ ràng.", 0),
        (base_q_texts[11], "N/A", "Không có phép toán chia trong module này.", 0),
        (base_q_texts[12], "Fail", "FE/src/pages/admin/SeatsPage.jsx & SeatFormPage.jsx: Không có API Bulk Create để tạo một lúc toàn bộ ma trận ghế cho phòng chiếu (80-120 ghế), phải tạo từng ghế gây lặp API và tốn tài nguyên.", 1),
        (base_q_texts[13], "Pass", "Cấu trúc if ngắn gọn, không lồng sâu.", 0),
        (base_q_texts[14], "Pass", "Các tham số tìm kiếm (search, roomId, rowNumber, seatType, status) khớp chuẩn giữa REST và DB.", 0),
        (base_q_texts[15], "Pass", "Không có biến thừa khai báo.", 0),
        (base_q_texts[16], "Pass", "Có chỉ mục phức hợp ExistsBySeatPosition(roomId, seatNumber, rowNumber) tối ưu tìm kiếm.", 0),
        (base_q_texts[17], "Pass", "Kiểm tra lỗi cẩn thận sau mỗi câu lệnh truy vấn database.", 0),
        (base_q_texts[18], "Pass", "Có hàm GetLockedSeatsByShowtime tích hợp Redis kiểm tra ghế đang bị khóa đồng thời.", 0),
        (base_q_texts[19], "Fail", "Luận văn Bảng 6 trang 36 quy định Exception 7 thông báo tiếng Việt: 'Ghế ngồi đã tồn tại', trong code trả về chuỗi tiếng Anh: 'seat position already exists in this room'.", 1)
    ]
    disc_seat = [
        "1. Điểm mạnh: Thiết kế sơ đồ ghế trực quan và linh hoạt, hỗ trợ 3 loại ghế với giá tiền khác nhau, hỗ trợ truy vấn ghế bị khóa đồng thời theo suất chiếu.",
        "2. Vấn đề phát hiện: Thiếu tính năng tạo hàng loạt (Bulk Insert) cho cả phòng chiếu; thiếu kiểm tra liên kết vé trước khi xóa ghế.",
        "3. Rủi ro lớn: Khi thiết lập phòng chiếu mới hàng trăm ghế, nhân viên phải thao tác thủ công nhiều lần hoặc viết script riêng ngoài hệ thống."
    ]
    create_j6_sheet("J6_SeatMgmt", 5, "Seat Management (Quản lý ghế ngồi)", "movie-service/internal/module/seat/business, repository, transport | FE/src/pages/admin/SeatsPage.jsx", q_seat, "Conditionally Approved", disc_seat)

    # -------------------------------------------------------------
    # CLUSTER 6: ONLINE BOOKING
    # -------------------------------------------------------------
    q_booking = [
        (base_q_texts[0], "Pass", "booking-service áp dụng kiến trúc Microservices hiện đại, tích hợp gRPC và Redis Mutex.", 0),
        (base_q_texts[1], "Pass", "Chú thích chi tiết luồng acquireDistributedSeatLocks và outbox client.", 0),
        (base_q_texts[2], "Pass", "Quy ước đặt tên biến rõ nghĩa (showtimeId, seatIds, totalAmount).", 0),
        (base_q_texts[3], "Pass", "Định dạng mã nguồn Go chuẩn gofmt.", 0),
        (base_q_texts[4], "Pass", "Tách riêng module outbox và gRPC client tái sử dụng giữa các hàm đặt vé.", 0),
        (base_q_texts[5], "Pass", "Không có dead code trong service booking.", 0),
        (base_q_texts[6], "Pass", "Kiểm tra con trỏ nil cho booking và seatsWithPrice an toàn.", 0),
        (base_q_texts[7], "Pass", "Kiểm tra danh sách seatIds rỗng trước khi xử lý.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo mảng tickets và outbox events đúng cấu trúc struct.", 0),
        (base_q_texts[9], "Fail", "FE/src/pages/client/PaymentPage.jsx: Khi người dùng từ chối (Reject) giao dịch MetaMask hoặc mạng blockchain bị lỗi timeout, hệ thống không gọi API giải phóng lock ghế ngay lập tức mà bắt người dùng chờ hết TTL 5 phút của Redis.", 1),
        (base_q_texts[10], "Pass", "Vòng lặp duyệt seatIds để lock và tạo ticket có kích thước cố định, dừng an toàn.", 0),
        (base_q_texts[11], "Fail", "booking-service/internal/services/booking.go lines 244-249: So sánh tiền tệ dùng kiểu float64 với dung sai 0.01 (clientTotal < expectedTotal-0.01 || clientTotal > expectedTotal+0.01) thay vì dùng số nguyên (int64/đồng) hoặc kiểu Decimal, tiềm ẩn rủi ro sai số làm tròn số học.", 1),
        (base_q_texts[12], "Pass", "Batch insert tickets qua datastore.BatchCreateTickets chia lô 500 bản ghi, tối ưu hiệu năng CSDL.", 0),
        (base_q_texts[13], "Pass", "Guard clauses xử lý kiểm tra tính hợp lệ rõ ràng, không lồng sâu.", 0),
        (base_q_texts[14], "Fail", "Luận văn Bảng 3 trang 31 quy định sau khi thanh toán thành công, hệ thống gửi email mã thông tin vé. Tuy nhiên việc gửi email phụ thuộc bất đồng bộ qua outbox và notification-service, nếu worker bị nghẽn thì người dùng không nhận được email ngay nhưng UI đã báo hoàn tất mà không có thông báo chờ.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa trong service.", 0),
        (base_q_texts[16], "Pass", "Truy vấn đặt vé và vé theo showtime_id và user_id có index B-tree đầy đủ.", 0),
        (base_q_texts[17], "Pass", "Tất cả các lệnh INSERT/UPDATE đều được kiểm tra lỗi và quản lý qua database transaction.", 0),
        (base_q_texts[18], "Pass", "ĐIỂM SÁNG XUẤT SẮC: Triển khai khóa phân tán Redis Mutex (5 phút) và Transactional Outbox Pattern chống race condition đặt trùng ghế và đảm bảo nhất quán dữ liệu phân tán.", 0),
        (base_q_texts[19], "Fail", "booking-service: Một số mã lỗi trả về chuỗi tiếng Anh như 'one or more seats are already locked' thay vì chuỗi tiếng Việt theo chuẩn Luận văn Bảng 3 ('Ghế bạn chọn đã được đặt, vui lòng chọn ghế khác').", 1)
    ]
    disc_booking = [
        "1. Điểm mạnh: Đây là module có chất lượng kỹ thuật cao nhất dự án! Sử dụng Redis Distributed Mutex Lock (5 phút) ngăn chặn hoàn toàn tình trạng đặt trùng ghế khi có hàng nghìn lượt truy cập đồng thời. Áp dụng Transactional Outbox Pattern đảm bảo tính nhất quán dữ liệu giữa Booking Service, Payment Service và Worker Service.",
        "2. Vấn đề phát hiện: So sánh giá tiền bằng số thực float64 tiềm ẩn rủi ro làm tròn; thiếu cơ chế giải phóng lock ghế chủ động khi hủy thanh toán Web3 MetaMask.",
        "3. Rủi ro lớn: Sai số làm tròn tiền tệ nếu áp dụng các mã giảm giá phức tạp hoặc thanh toán quy đổi tỷ giá Ethereum/VND."
    ]
    create_j6_sheet("J6_OnlineBooking", 6, "Online Booking (Đặt vé trực tuyến)", "booking-service/internal/services/booking.go | FE/src/pages/client/BookingPage.jsx, PaymentPage.jsx", q_booking, "Conditionally Approved (Chất lượng kỹ thuật rất tốt, cần chuẩn hóa tiền tệ)", disc_booking)

    # -------------------------------------------------------------
    # CLUSTER 7: BOX OFFICE BOOKING
    # -------------------------------------------------------------
    q_boxoffice = [
        (base_q_texts[0], "Pass", "Module bán vé tại quầy trên Frontend phân chia rõ ràng các bước: Chọn suất chiếu -> Chọn ghế -> Thanh toán tiền mặt.", 0),
        (base_q_texts[1], "Pass", "Có chú thích rõ ràng các hàm searchByBookingId và markTicketAsUsed.", 0),
        (base_q_texts[2], "Pass", "Tên biến, hàm đồng nhất giữa frontend và backend.", 0),
        (base_q_texts[3], "Pass", "Giao diện BoxOfficePage.jsx thiết kế theo chuẩn POS bán vé rạp.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng bookingService và showtimeService chung với client portal.", 0),
        (base_q_texts[5], "Fail", "FE/src/pages/admin/TicketSearchPage.jsx line 54: Chứa đoạn mã delay giả tạo không cần thiết 'await delay(1500)' làm chậm tốc độ tra cứu vé 1.5 giây một cách vô lý.", 1),
        (base_q_texts[6], "Pass", "Kiểm tra mảng ticketsData an toàn trước khi render.", 0),
        (base_q_texts[7], "Pass", "Không có thao tác index ngoài biên mảng.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo state showtimes và tickets đúng kiểu mảng rỗng.", 0),
        (base_q_texts[9], "Fail", "BoxOfficePage.jsx: Khi nhân viên chọn một suất chiếu đã quá giờ chiếu nhưng chưa đổi trạng thái trong CSDL, hệ thống vẫn cho phép chọn ghế và chỉ báo lỗi khi submit thanh toán, gây lãng phí thao tác của thu ngân.", 1),
        (base_q_texts[10], "Pass", "Vòng lặp render ghế tại quầy có key duy nhất và điều kiện dừng rõ ràng.", 0),
        (base_q_texts[11], "N/A", "Không có phép chia trong module.", 0),
        (base_q_texts[12], "Pass", "Không có query trong loop.", 0),
        (base_q_texts[13], "Pass", "Cấu trúc điều kiện phẳng, dễ đọc.", 0),
        (base_q_texts[14], "Fail", "Luận văn Bảng 20 trang 37 quy định Use case 'Xuất vé' cho phép in vé giấy cho khách. Thực tế code chỉ cập nhật trạng thái đã dùng (markTicketAsUsed) và mở modal xem trước, chưa tích hợp chức năng in nhiệt (print command/PDF) thực tế.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa trong component.", 0),
        (base_q_texts[16], "Pass", "Tra cứu vé theo booking_id tận dụng index Primary Key và Foreign Key trong PostgreSQL.", 0),
        (base_q_texts[17], "Pass", "Kiểm tra response.code !== 200 và xử lý try-catch đầy đủ.", 0),
        (base_q_texts[18], "Pass", "Bán vé tại quầy cũng sử dụng chung luồng lock ghế Redis như Online Booking để tránh tranh chấp ghế với khách đặt qua mạng.", 0),
        (base_q_texts[19], "Pass", "Thông báo lỗi tiếng Việt tại màn hình tra cứu vé rõ ràng ('Không thể tìm kiếm vé', 'Không tìm thấy vé').", 0)
    ]
    disc_boxoffice = [
        "1. Điểm mạnh: Giao diện bán vé tại quầy (POS) trực quan, nhân viên thao tác nhanh; dùng chung hạ tầng khóa phân tán Redis chống bán trùng ghế với khách mua online.",
        "2. Vấn đề phát hiện: Phát hiện đoạn mã 'await delay(1500)' giả tạo gây chậm trễ vô cớ khi tra cứu vé; tính năng in vé giấy (Xuất vé) mới chỉ dừng ở mức đổi trạng thái trên phần mềm, chưa hỗ trợ lệnh in thực tế.",
        "3. Rủi ro lớn: Cần xóa ngay đoạn delay giả tạo để đảm bảo thời gian phản hồi đạt tiêu chuẩn < 200ms theo kế hoạch SQA."
    ]
    create_j6_sheet("J6_BoxOffice", 7, "Box Office Booking (Bán vé tại quầy & Xuất vé)", "FE/src/pages/admin/BoxOfficePage.jsx, TicketSearchPage.jsx | booking-service", q_boxoffice, "Conditionally Approved", disc_boxoffice)

    # -------------------------------------------------------------
    # CLUSTER 8: STAFF & PERMISSION
    # -------------------------------------------------------------
    q_staff = [
        (base_q_texts[0], "Pass", "Mã nguồn phân quyền tuân thủ chuẩn RBAC (Role-Based Access Control) với 4 vai trò chính.", 0),
        (base_q_texts[1], "Pass", "Có chú thích rõ ràng các quyền: movie_manage, showtime_manage, seat_manage, report_view...", 0),
        (base_q_texts[2], "Pass", "Quy ước đặt mã quyền theo snake_case và tên role chuẩn xác.", 0),
        (base_q_texts[3], "Pass", "Định dạng code đồng bộ với toàn bộ dự án.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng permissionService và roleController cho việc cấp phát quyền.", 0),
        (base_q_texts[5], "Pass", "Không có mã rác trong module quản lý nhân viên.", 0),
        (base_q_texts[6], "Pass", "Kiểm tra null/undefined của rolePermissions map an toàn.", 0),
        (base_q_texts[7], "Pass", "Không có lỗi truy xuất mảng vượt giới hạn.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo state roles, permissions và rolePermissions map chính xác.", 0),
        (base_q_texts[9], "Pass", "Kiểm tra quyền truy cập đúng đắn: chỉ Admin mới có quyền vào trang phân quyền.", 0),
        (base_q_texts[10], "Pass", "Vòng lặp phân quyền có điều kiện kết thúc rõ ràng.", 0),
        (base_q_texts[11], "N/A", "Không có phép toán chia trong module này.", 0),
        (base_q_texts[12], "Fail", "FE/src/pages/admin/PermissionManagementPage.jsx lines 42-48: Lỗi N+1 request - Gửi tuần tự từng request lấy quyền của từng role trong vòng lặp for (await permissionService.getRolePermissions(role.id)) thay vì gọi song song hoặc gom API.", 1),
        (base_q_texts[13], "Pass", "Độ sâu lồng if không quá 2 cấp.", 0),
        (base_q_texts[14], "Fail", "Luận văn Hình 27 trang 60 mô tả luồng tạo tài khoản nhân viên có bước generatePassword() tự động và gửi qua email. Trong code StaffFormPage.jsx admin phải nhập tay mật khẩu hoặc fix cứng mà không tự sinh mật khẩu gửi mail.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa khai báo.", 0),
        (base_q_texts[16], "Pass", "Bảng tblRolePermission có composite index (role_id, permission_id) tối ưu truy vấn.", 0),
        (base_q_texts[17], "Pass", "Kiểm tra lỗi đầy đủ sau các thao tác gán/hủy quyền trong DB.", 0),
        (base_q_texts[18], "Fail", "auth-service & user-service: Khi Quản trị viên cập nhật lại danh sách quyền của một Role, hệ thống xóa cache trên Redis nhưng JWT token cũ của người dùng vẫn có hiệu lực (24h) và chứa quyền cũ, chưa có cơ chế thu hồi token tức thì (Token Blacklist).", 1),
        (base_q_texts[19], "Pass", "Thông báo thành công và lỗi bằng tiếng Anh/Việt tương đối rõ ràng.", 0)
    ]
    disc_staff = [
        "1. Điểm mạnh: Hệ thống RBAC được thiết kế bài bản với 4 vai trò, 14 mã quyền chi tiết, lưu trữ quan hệ nhiều - nhiều giữa roles và permissions.",
        "2. Vấn đề phát hiện: Vòng lặp lấy quyền từng role gây lỗi N+1 network request; Luồng tạo nhân viên chưa có chức năng tự sinh mật khẩu ngẫu nhiên gửi email như trong sơ đồ tuần tự luận văn.",
        "3. Rủi ro lớn: Thu hồi hoặc giáng quyền của nhân viên không có hiệu lực ngay lập tức trên các request đã có JWT token (phải chờ token hết hạn sau 24h)."
    ]
    create_j6_sheet("J6_StaffPermission", 8, "Staff & Permission (Quản lý nhân viên & Phân quyền)", "FE/src/pages/admin/StaffPage.jsx, PermissionManagementPage.jsx | user-service, auth-service", q_staff, "Conditionally Approved", disc_staff)

    # -------------------------------------------------------------
    # CLUSTER 9: REVENUE ANALYTICS
    # -------------------------------------------------------------
    q_analytics = [
        (base_q_texts[0], "Pass", "analytics-service viết bằng TypeScript với kiến trúc microservice rõ ràng, giao tiếp gRPC.", 0),
        (base_q_texts[1], "Pass", "Có chú thích giải thích công thức tổng hợp doanh thu theo thời gian và theo phim.", 0),
        (base_q_texts[2], "Pass", "Quy ước đặt tên biến chuẩn TypeScript (RevenueByMovie, AnalyticsFilters).", 0),
        (base_q_texts[3], "Pass", "Giao diện RevenueStatsPage.jsx tích hợp thư viện Recharts vẽ biểu đồ chuyên nghiệp.", 0),
        (base_q_texts[4], "Pass", "Tái sử dụng các tiện ích định dạng tiền tệ formatCurrency và dateUtils.", 0),
        (base_q_texts[5], "Fail", "FE/src/pages/admin/RevenueStatsPage.jsx line 66: Gán cứng genre: 'N/A' (Dead/Dummy code), trong khi Luận văn Bảng 12 trang 32 quy định rõ usecase thống kê doanh thu theo thể loại phim (Flow bước 7 và 8).", 1),
        (base_q_texts[6], "Pass", "Kiểm tra an toàn timeData.success và movieRevenueData.data trước khi map.", 0),
        (base_q_texts[7], "Pass", "Không có lỗi truy cập mảng ngoài biên.", 0),
        (base_q_texts[8], "Pass", "Khởi tạo state Recharts dạng mảng rỗng mặc định an toàn.", 0),
        (base_q_texts[9], "Pass", "Các nhánh kiểm tra date range và filter thời gian hoạt động đúng đắn.", 0),
        (base_q_texts[10], "Pass", "Vòng lặp tổng hợp doanh thu theo phim có tập hợp showtimeId hữu hạn, dừng an toàn.", 0),
        (base_q_texts[11], "Pass", "RevenueStatsPage.jsx lines 88-89: Đã kiểm tra mẫu số totalTickets > 0 trước khi tính giá vé trung bình (averageTicketPrice = totalRevenue / totalTickets), tránh hoàn toàn lỗi Division by Zero.", 0),
        (base_q_texts[12], "Pass", "Gom nhóm showtimeIds trước khi gọi movieGrpcClient.getShowtimes để tránh N+1 gRPC call.", 0),
        (base_q_texts[13], "Pass", "Cấu trúc if lồng tối đa 2 cấp.", 0),
        (base_q_texts[14], "Fail", "analytics-service/src/services/analytics-service.ts lines 26 & 82: Gọi 'await redisClient.set(cacheKey, JSON.stringify(data), 300)'. Trong Node Redis v4, cú pháp set với TTL là set(key, value, { EX: 300 }) hoặc setEx(key, 300, value); truyền số 300 là sai tham số hình thức và làm mất tác dụng hết hạn TTL của cache.", 1),
        (base_q_texts[15], "Pass", "Không có biến thừa khai báo trong service.", 0),
        (base_q_texts[16], "Pass", "Truy vấn tổng hợp theo thời gian tận dụng index trên created_at và status của tblBooking.", 0),
        (base_q_texts[17], "Pass", "Kiểm tra lỗi đầy đủ sau các lệnh gọi gRPC từ booking-service và movie-service.", 0),
        (base_q_texts[18], "Pass", "Dữ liệu thống kê chỉ đọc (Read-only) và được cache trên Redis 300 giây để giảm tải cho DB.", 0),
        (base_q_texts[19], "Fail", "Giao diện biểu đồ Recharts và các tiêu đề bộ lọc còn hiển thị nhiều từ tiếng Anh ('Overview', 'Total Revenue', 'Tickets Sold') chưa được Việt hóa đồng bộ theo yêu cầu luận văn.", 1)
    ]
    disc_analytics = [
        "1. Điểm mạnh: Giao diện biểu đồ doanh thu trực quan, đa dạng (BarChart, LineChart, PieChart), có kiểm tra mẫu số an toàn chống lỗi chia cho 0; tổng hợp dữ liệu đa nguồn từ Booking Service và Movie Service qua gRPC.",
        "2. Vấn đề phát hiện: Tính năng thống kê doanh thu theo thể loại phim bị hardcode 'N/A' (chưa hoàn thiện); gọi sai cú pháp TTL trên Redis v4 làm mất tác dụng hết hạn cache.",
        "3. Rủi ro lớn: Thiếu TTL trên Redis khiến bộ nhớ cache phình to theo thời gian gây tràn RAM server phân tích."
    ]
    create_j6_sheet("J6_RevenueAnalytics", 9, "Revenue Analytics (Thống kê báo cáo doanh thu)", "analytics-service/src/services/analytics-service.ts | FE/src/pages/admin/RevenueStatsPage.jsx", q_analytics, "Conditionally Approved", disc_analytics)

    # -------------------------------------------------------------
    # 3. SHEET: J7_TestPlan_TestCase
    # -------------------------------------------------------------
    ws_j7 = wb.create_sheet(title="J7_TestPlan_TestCase")
    ws_j7.views.sheetView[0].showGridLines = True

    # Header block for J7
    ws_j7.cell(row=1, column=1, value="Project Name:").font = meta_label_font
    ws_j7.cell(row=1, column=2, value="Xây dựng hệ thống quản lý rạp chiếu phim (Cinema Booking System)").font = meta_val_font

    ws_j7.cell(row=2, column=1, value="Reviewed Document:").font = meta_label_font
    ws_j7.cell(row=2, column=2, value="Tài liệu SQA_Plan_Updated (2).docx, Luận văn tốt nghiệp (Chương 3) & Bộ Test Cases").font = meta_val_font

    ws_j7.cell(row=3, column=1, value="Reviewed Feature/Scope:").font = meta_label_font
    ws_j7.cell(row=3, column=2, value="Checklist for Test Plan (Items 1-5) & Test Cases (Items 1-8) theo Table J.7 (Mastering SQA)").font = meta_val_font

    j7_questions = [
        # Test Plan Checklist (Items 1 to 5)
        ("TP-01", "Kế hoạch kiểm thử có phản ánh đầy đủ các yêu cầu nghiệp vụ và kỹ thuật của hệ thống không? (Does the plan reflect the requirements?)", "Pass", "SQA Plan mục 1.1 và 6.2 đã xác định phạm vi kiểm thử 100% bao phủ các phân hệ cốt lõi: Đặt vé, Thanh toán, Phim, Phòng, Ghế, RBAC, Chatbot RAG.", 0),
        ("TP-02", "Tiêu chí nghiệm thu (Acceptance Criteria) cho kế hoạch kiểm thử chấp nhận đã được xác định cụ thể chưa? (Have acceptance criteria been specified?)", "Pass", "SQA Plan mục 6.2 đã quy định tiêu chí Đạt/Không đạt rõ ràng: 100% test case thực thi, không còn lỗi nghiêm trọng/cao, tỷ lệ loại bỏ lỗi đạt >= 90%.", 0),
        ("TP-03", "Chiến lược kiểm thử có đầy đủ và thích hợp để phát hiện mọi lỗi tiềm ẩn không? (Is the test strategy adequate to uncover all defects?)", "Pass", "Chiến lược áp dụng mô hình McCall đa chiều (Correctness, Reliability 10.000 CCU, Integrity, Usability, Maintainability, Portability).", 0),
        ("TP-04a", "Mô tả kiểm thử có bao gồm Mục tiêu kiểm thử (Test objectives) không?", "Pass", "SQA Plan mục 1.2 và 6.3 nêu rõ mục tiêu từng phân hệ kiểm thử.", 0),
        ("TP-04b", "Mô tả kiểm thử có bao gồm Dữ liệu đầu vào (Test inputs) không?", "Pass", "Đã quy định các tập dữ liệu hợp lệ, biên và không hợp lệ.", 0),
        ("TP-04c", "Mô tả kiểm thử có bao gồm Kết quả đầu ra mong đợi (Test outputs) không?", "Pass", "Mỗi kịch bản kiểm thử đều có mô tả kết quả mong đợi tương ứng.", 0),
        ("TP-04d", "Mô tả kiểm thử có bao gồm Quy trình/Các bước kiểm thử (Test procedures) không?", "Pass", "Mô tả các bước thực hiện tuần tự rõ ràng.", 0),
        ("TP-04e", "Mô tả kiểm thử có bao gồm Trình tự kiểm thử (Test sequence) giữa các cấp độ không?", "Fail", "SQA_Plan_Updated (2).docx chưa mô tả rõ trình tự kiểm thử (Test Sequence) giữa các cấp độ kiểm thử (ví dụ: thứ tự kiểm thử tích hợp giữa Booking Service và Payment Service theo kịch bản Outbox).", 1),
        ("TP-05", "Kế hoạch kiểm thử có liệt kê đầy đủ yêu cầu kiểm thử như lịch trình (Test schedule) và tài nguyên (Resources) không?", "Fail", "SQA Plan mục 4 có phân vai trò chung nhưng thiếu lịch trình chi tiết (Gantt chart/Milestones) và bảng phân bổ tài nguyên kiểm thử cụ thể theo ngày/tuần.", 1),
        # Test Cases Checklist (Items 1 to 8)
        ("TC-01", "Mỗi test case có chỉ rõ điều kiện kiểm thử, quy trình thực hiện và kết quả mong đợi không?", "Pass", "Tất cả các test case đều có đủ 3 thành phần: Pre-conditions, Steps, Expected Results.", 0),
        ("TC-02", "Kết quả thực tế có được ghi chép đầy đủ chi tiết và trung thực không?", "Pass", "Ghi nhận đầy đủ trạng thái Pass/Fail và mô tả chi tiết lỗi phát hiện.", 0),
        ("TC-03a", "Các test case xác thực trường, bản ghi và cập nhật CSDL có bao gồm điều kiện hợp lệ (Valid conditions) không?", "Pass", "Bao phủ đầy đủ các trường hợp dữ liệu chuẩn xác (Happy path).", 0),
        ("TC-03b", "Các test case có bao gồm điều kiện không hợp lệ (Invalid conditions) không?", "Pass", "Có test case kiểm tra nhập sai định dạng email, sai mật khẩu, trùng lịch chiếu, phòng chiếu không tồn tại.", 0),
        ("TC-03c", "Các test case có bao gồm các điều kiện bất thường hoặc hiếm gặp (Unexpected / unusual conditions) không?", "Fail", "Bộ test case trong luận văn chưa bao phủ các kịch bản ngoại lệ bất thường: ngắt mạng khi đang thanh toán MetaMask, Redis sập khi đang giữ lock ghế, lỗi timeout cổng thanh toán bên thứ ba.", 1),
        ("TC-03d", "Các test case có bao gồm điều kiện biên (Boundary conditions) không?", "Pass", "Có kiểm thử biên độ dài mật khẩu (min 6 ký tự), phân trang (limit=0, limit=100), dung sai tiền tệ (0.01).", 0),
        ("TC-04", "Các test case cho báo cáo thống kê có bao gồm dữ liệu thử nghiệm cùng kết quả đầu ra mong đợi không?", "Pass", "Test case thống kê doanh thu có dữ liệu lọc theo ngày bắt đầu/kết thúc và doanh thu kỳ vọng.", 0),
        ("TC-05", "Tất cả các chức năng nghiệp vụ quy định trong phạm vi đã được đưa vào bộ test case chưa?", "Pass", "Bao phủ đầy đủ các use case nghiệp vụ từ UC01 đến UC20.", 0),
        ("TC-06", "Các chức năng nghiệp vụ trong test case có nhất quán với mô tả trong tài liệu đặc tả yêu cầu (SRS/Luận văn) không?", "Fail", "Tồn tại sự không nhất quán lớn: Đặc tả Luận văn Bảng 1 mô tả 1 form đăng nhập chung cho cả 4 tác nhân, nhưng thực tế chia 2 cổng riêng biệt (khách hàng /login và admin /admin/login); Bảng 2 đặc tả đăng ký bị nhầm lỗi của đăng nhập.", 1),
        ("TC-07", "Tiêu chuẩn cho từng chức năng cấu trúc đã được công bố rõ ràng chưa?", "Pass", "Tiêu chuẩn về phân quyền RBAC và mã trạng thái HTTP (200, 400, 403, 500) được định nghĩa đầy đủ.", 0),
        ("TC-08", "Tất cả các yêu cầu nghiệp vụ có thể truy vết được tới các test case tương ứng không (Traceability)?", "Fail", "Chưa xây dựng Ma trận truy vết yêu cầu (Requirements Traceability Matrix - RTM) để liên kết 2 chiều giữa mã yêu cầu chức năng (FR) trong Luận văn và mã Test Case.", 1)
    ]

    j7_pass = sum(1 for q in j7_questions if q[2] == "Pass")
    j7_fail = sum(1 for q in j7_questions if q[2] == "Fail")
    j7_na = sum(1 for q in j7_questions if q[2] == "N/A")
    j7_err = sum(q[4] for q in j7_questions)

    ws_j7.cell(row=4, column=1, value="Number of Pass / Fail / N/A / Number of Errors:").font = meta_label_font
    ws_j7.cell(row=4, column=2, value=f"Pass: {j7_pass} | Fail: {j7_fail} | N/A: {j7_na} | Number of Errors: {j7_err}").font = meta_val_font
    ws_j7.cell(row=4, column=3, value=f"Total: {len(j7_questions)} (Pass: {j7_pass}, Fail: {j7_fail}, N/A: {j7_na})").font = meta_label_font
    ws_j7.cell(row=4, column=4, value=f"Errors Counted: {j7_err}").font = meta_label_font

    ws_j7.cell(row=5, column=1, value="Quick Counters:").font = meta_label_font
    ws_j7.cell(row=5, column=2, value=f"Pass: {j7_pass}").font = pass_font
    ws_j7.cell(row=5, column=3, value=f"Fail: {j7_fail}").font = fail_font
    ws_j7.cell(row=5, column=4, value=f"N/A: {j7_na}").font = na_font

    for r in range(1, 6):
        ws_j7.row_dimensions[r].height = 20
        ws_j7.cell(row=r, column=1).fill = meta_fill
        for c in range(1, 5):
            ws_j7.cell(row=r, column=c).border = Border(bottom=Side(style="thin", color="E0E0E0"))

    j7_headers = ["Item No.", "Checklist Question (Theo Table J.7 - Mastering SQA)", "Review Result (Pass / Fail / N/A)", "Notes (for Fail, NA case please explain in detail, list all error you found)"]
    ws_j7.row_dimensions[6].height = 26
    for c_idx, h_text in enumerate(j7_headers, 1):
        cell = ws_j7.cell(row=6, column=c_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = header_border

    j7_curr_row = 7
    for q_item in j7_questions:
        item_no, q_text, q_res, q_notes, _ = q_item
        ws_j7.row_dimensions[j7_curr_row].height = 36 if len(q_notes) > 80 else 24

        c1 = ws_j7.cell(row=j7_curr_row, column=1, value=item_no)
        c1.font = data_bold
        c1.alignment = center_align
        c1.border = cell_border

        c2 = ws_j7.cell(row=j7_curr_row, column=2, value=q_text)
        c2.font = data_font
        c2.alignment = wrap_left_align
        c2.border = cell_border

        c3 = ws_j7.cell(row=j7_curr_row, column=3, value=q_res)
        c3.alignment = center_align
        c3.border = cell_border
        if q_res == "Pass":
            c3.font = pass_font
            c3.fill = pass_fill
        elif q_res == "Fail":
            c3.font = fail_font
            c3.fill = fail_fill
        else:
            c3.font = na_font
            c3.fill = na_fill

        c4 = ws_j7.cell(row=j7_curr_row, column=4, value=q_notes)
        c4.font = data_font
        c4.alignment = wrap_left_align
        c4.border = cell_border

        j7_curr_row += 1

    # Conclusion and Discussion for J7
    j7_curr_row += 1
    ws_j7.row_dimensions[j7_curr_row].height = 22
    ws_j7.cell(row=j7_curr_row, column=1, value="Conclusion:").font = meta_label_font
    ws_j7.cell(row=j7_curr_row, column=2, value="Conditionally Approved (Phê duyệt có điều kiện)").font = data_bold

    j7_curr_row += 1
    ws_j7.row_dimensions[j7_curr_row].height = 22
    ws_j7.cell(row=j7_curr_row, column=1, value="Discussion:").font = meta_label_font
    ws_j7.cell(row=j7_curr_row, column=2, value="1. Điểm mạnh: Kế hoạch SQA được xây dựng rất công phu, bám sát cấu trúc IEEE 730 và mô hình chất lượng McCall đa chiều; bao phủ đầy đủ các phân hệ chức năng từ đặt vé, thanh toán đến chatbot RAG.").font = discussion_font

    j7_discussion = [
        "2. Vấn đề phát hiện: Thiếu ma trận truy vết yêu cầu (RTM) để liên kết mã yêu cầu với mã test case; thiếu kịch bản kiểm thử điều kiện bất thường (mạng chập chờn khi gửi giao dịch crypto, redis failover); tài liệu đặc tả có một số chỗ vênh so với mã nguồn thực tế.",
        "3. Rủi ro lớn: Nếu không có RTM, khi có sự thay đổi nghiệp vụ (Change Request) trong đồ án sẽ rất khó kiểm soát và đánh giá phạm vi ảnh hưởng (Impact Analysis) đến bộ test case hồi quy."
    ]
    for d_line in j7_discussion:
        j7_curr_row += 1
        ws_j7.row_dimensions[j7_curr_row].height = 20
        ws_j7.cell(row=j7_curr_row, column=2, value=d_line).font = discussion_font

    ws_j7.column_dimensions["A"].width = 12
    ws_j7.column_dimensions["B"].width = 46
    ws_j7.column_dimensions["C"].width = 18
    ws_j7.column_dimensions["D"].width = 65

    # -------------------------------------------------------------
    # 4. SHEET: Prompts_Used
    # -------------------------------------------------------------
    ws_prompts = wb.create_sheet(title="Prompts_Used")
    ws_prompts.views.sheetView[0].showGridLines = True

    ws_prompts.cell(row=1, column=1, value="DANH MỤC CÁC PROMPT VÀ PHƯƠNG PHÁP LUẬN SỬ DỤNG (PROMPTS USED)").font = title_font
    ws_prompts.cell(row=2, column=1, value="Dự án: Xây dựng hệ thống quản lý rạp chiếu phim (Cinema Booking System)").font = subtitle_font

    p_headers = ["Prompt ID", "Nhiệm vụ (Task)", "Nội dung chỉ dẫn (Prompt Content)", "Kết quả đầu ra (Output)"]
    ws_prompts.row_dimensions[4].height = 26
    for c_idx, h_text in enumerate(p_headers, 1):
        cell = ws_prompts.cell(row=4, column=c_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = header_border

    prompts_data = [
        ("PR_01", "Xây dựng bảng kiểm J6 cho Microservices", "Từ Bảng J.6 (Mastering SQA): Loại bỏ các câu hỏi đặc thù ngôn ngữ C (phép toán con trỏ C). Thêm các câu hỏi kiểm tra Microservices, Go Clean Architecture, React Hooks, Redis Mutex Lock, Transactional Outbox, JWT RBAC và Joi validation. Tạo 20 câu hỏi chuẩn hóa.", "Checklist J6 gồm 20 câu hỏi chuẩn hóa áp dụng đồng bộ cho các phân hệ chức năng."),
        ("PR_02", "Kiểm tra mã nguồn 9 phân hệ chức năng", "Rà soát toàn bộ mã nguồn của 9 phân hệ chức năng (Room, Seat, Box Office, Online Booking, Login, Registration, Edit Profile, Staff & Permission, Revenue Analytics). Với mỗi lỗi Fail, chỉ rõ đường dẫn file, số dòng chính xác và chi tiết lỗi. Không gộp chung vào một sheet duy nhất.", "9 sheet kiểm tra mã nguồn độc lập với bằng chứng file và số dòng cụ thể."),
        ("PR_03", "Kiểm tra Kế hoạch SQA và Test Cases (J7)", "Sử dụng Bảng J.7 (Mastering SQA) để đánh giá tài liệu SQA_Plan_Updated (2).docx và bộ Test Cases đối chiếu với Luận văn tốt nghiệp và bài giảng SQA. Chỉ ra các mục còn thiếu (RTM, Test Sequence, Test Schedule, điều kiện bất thường).", "Sheet kiểm tra J7_TestPlan_TestCase với 5 lỗi phát hiện và đề xuất khắc phục cụ thể.")
    ]

    for r_idx, p_data in enumerate(prompts_data, 5):
        ws_prompts.row_dimensions[r_idx].height = 36
        for c_idx, val in enumerate(p_data, 1):
            cell = ws_prompts.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.border = cell_border
            if c_idx == 1:
                cell.alignment = center_align
                cell.font = data_bold
            else:
                cell.alignment = wrap_left_align

    ws_prompts.column_dimensions["A"].width = 14
    ws_prompts.column_dimensions["B"].width = 30
    ws_prompts.column_dimensions["C"].width = 50
    ws_prompts.column_dimensions["D"].width = 45

    # Remove default sheet
    wb.remove(default_sheet)

    # Save to 4_review.xlsx
    target_path = r"c:\Users\ADMIN\Documents\cinema-project-main\4_review.xlsx"
    wb.save(target_path)
    print(f"Excel file created successfully at: {target_path}")

if __name__ == "__main__":
    build_excel()

