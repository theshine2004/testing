# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_system_test_excel():
    wb = openpyxl.Workbook()
    default_sheet = wb.active

    # Styling definitions
    font_name = "Calibri"
    title_font = Font(name=font_name, size=13, bold=True, color="1F4E79")
    section_font = Font(name=font_name, size=11, bold=True, color="1F4E79")
    meta_label_font = Font(name=font_name, size=10, bold=True, color="1F4E79")
    meta_val_font = Font(name=font_name, size=10, color="000000")
    header_font = Font(name=font_name, size=10, bold=True, color="FFFFFF")
    data_font = Font(name=font_name, size=10, color="000000")
    data_bold = Font(name=font_name, size=10, bold=True, color="000000")
    pass_font = Font(name=font_name, size=10, bold=True, color="276A3C")
    fail_font = Font(name=font_name, size=10, bold=True, color="9C0006")
    na_font = Font(name=font_name, size=10, bold=True, color="7F7F7F")
    disc_font = Font(name=font_name, size=10, color="1F3864")

    # Fills
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    sub_header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    meta_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fail_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    na_fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    alert_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    # Borders
    thin_border = Side(border_style="thin", color="D9D9D9")
    dark_border = Side(border_style="thin", color="8EA9DB")
    cell_border = Border(left=thin_border, right=thin_border, top=thin_border, bottom=thin_border)
    header_border = Border(left=thin_border, right=thin_border, top=dark_border, bottom=dark_border)

    # Alignments
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    wrap_left_align = Alignment(horizontal="left", vertical="top", wrap_text=True)
    wrap_center_align = Alignment(horizontal="center", vertical="top", wrap_text=True)

    def create_sheet(ws, title, uc_id, uc_name, scope_desc, stats, eval_info, test_cases, conclusion, discussions):
        ws.views.sheetView[0].showGridLines = True
        
        # 1. TIÊU ĐỀ CHÍNH
        ws.cell(row=1, column=1, value=f"BÁO CÁO KIỂM THỬ HỆ THỐNG (SYSTEM TEST REPORT) — {uc_name.upper()}").font = title_font
        ws.cell(row=2, column=1, value="Dự án: Xây dựng hệ thống quản lý rạp chiếu phim (Cinema Booking System)").font = meta_val_font
        ws.cell(row=3, column=1, value=f"Phạm vi kiểm thử: {scope_desc}").font = meta_val_font

        # 2. PHẦN 1: BẢNG THỐNG KÊ
        ws.cell(row=5, column=1, value="PHẦN 1: BẢNG THỐNG KÊ").font = section_font
        stat_headers = ["STT", "Use case", "TESTED", "PASS", "FAIL", "N/A"]
        ws.row_dimensions[6].height = 24
        for c_idx, h_text in enumerate(stat_headers, 1):
            c = ws.cell(row=6, column=c_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = header_border

        # Data row of stat table
        ws.row_dimensions[7].height = 22
        ws.cell(row=7, column=1, value=1).alignment = center_align
        ws.cell(row=7, column=2, value=f"{uc_id}: {uc_name}").alignment = left_align
        ws.cell(row=7, column=3, value=stats["tested"]).alignment = center_align
        ws.cell(row=7, column=4, value=stats["pass"]).alignment = center_align
        ws.cell(row=7, column=5, value=stats["fail"]).alignment = center_align
        ws.cell(row=7, column=6, value=stats["na"]).alignment = center_align

        for col in range(1, 7):
            cell = ws.cell(row=7, column=col)
            cell.font = data_font
            cell.border = cell_border
            if col == 4:
                cell.fill = pass_fill
                cell.font = pass_font
            elif col == 5:
                cell.fill = fail_fill
                cell.font = fail_font

        # Total row of stat table
        ws.row_dimensions[8].height = 22
        ws.cell(row=8, column=1, value="Tổng").alignment = center_align
        ws.cell(row=8, column=2, value="").alignment = left_align
        ws.cell(row=8, column=3, value=stats["tested"]).alignment = center_align
        ws.cell(row=8, column=4, value=stats["pass"]).alignment = center_align
        ws.cell(row=8, column=5, value=stats["fail"]).alignment = center_align
        ws.cell(row=8, column=6, value=stats["na"]).alignment = center_align
        for col in range(1, 7):
            cell = ws.cell(row=8, column=col)
            cell.font = data_bold
            cell.fill = total_fill
            cell.border = cell_border

        ws.cell(row=10, column=1, value="Nhận xét chung:").font = meta_label_font
        ws.cell(row=10, column=2, value=stats["general_comment"]).font = meta_val_font
        ws.cell(row=11, column=1, value="Thông tin chung:").font = meta_label_font
        ws.cell(row=11, column=2, value=stats["general_info"]).font = meta_val_font

        # 3. PHẦN 2: PHẦN ĐÁNH GIÁ
        ws.cell(row=13, column=1, value="PHẦN 2: PHẦN ĐÁNH GIÁ (SQA EVALUATION & SIGN-OFF)").font = section_font
        eval_headers = ["Mục", "Nội dung"]
        ws.row_dimensions[14].height = 24
        for c_idx, h_text in enumerate(eval_headers, 1):
            c = ws.cell(row=14, column=c_idx, value=h_text)
            c.font = header_font
            c.fill = sub_header_fill
            c.alignment = center_align
            c.border = header_border

        eval_rows = [
            ("Tên dự án", "Xây dựng website quản lý rạp chiếu phim (Cinema Booking System)"),
            ("Nội dung kiểm thử", eval_info["content"]),
            ("Quy chuẩn đối chiếu", "Luận văn tốt nghiệp (graduation_thesis.pdf), SQA Plan theo chuẩn IEEE 730 & mô hình McCall"),
            ("Kết luận phê duyệt", conclusion),
        ]
        curr_r = 15
        for item, content in eval_rows:
            ws.row_dimensions[curr_r].height = 22
            c1 = ws.cell(row=curr_r, column=1, value=item)
            c1.font = meta_label_font
            c1.fill = meta_fill
            c1.alignment = left_align
            c1.border = cell_border

            c2 = ws.cell(row=curr_r, column=2, value=content)
            c2.font = data_bold if item == "Kết luận phê duyệt" else data_font
            c2.alignment = left_align
            c2.border = cell_border
            if item == "Kết luận phê duyệt":
                c2.fill = alert_fill
                c2.font = fail_font
            curr_r += 1

        # Evaluation Statistics Table
        curr_r += 1
        ws.cell(row=curr_r, column=1, value="Thống kê kiểm thử").font = section_font
        curr_r += 1
        thongke_headers = ["Trạng thái", "Số lượng", "Định nghĩa"]
        ws.row_dimensions[curr_r].height = 22
        for c_idx, h_text in enumerate(thongke_headers, 1):
            c = ws.cell(row=curr_r, column=c_idx, value=h_text)
            c.font = header_font
            c.fill = header_fill
            c.alignment = center_align
            c.border = header_border

        curr_r += 1
        thongke_data = [
            ("TESTED", stats["tested"], "Tổng số ca kiểm thử hệ thống đã thiết kế và thực thi đầy đủ"),
            ("PASS", stats["pass"], "Ca kiểm thử đạt yêu cầu mong đợi, hệ thống xử lý đúng nghiệp vụ và an toàn"),
            ("FAIL", stats["fail"], "Ca kiểm thử phát hiện lỗi (lệch đặc tả, lỗi logic, lỗi bảo mật, tính năng chưa hoàn thiện)"),
            ("N/A", stats["na"], "Không áp dụng hoặc không khả dụng")
        ]
        for st_name, st_qty, st_def in thongke_data:
            ws.row_dimensions[curr_r].height = 20
            c1 = ws.cell(row=curr_r, column=1, value=st_name)
            c1.alignment = center_align
            c1.border = cell_border
            if st_name == "PASS":
                c1.fill = pass_fill
                c1.font = pass_font
            elif st_name == "FAIL":
                c1.fill = fail_fill
                c1.font = fail_font
            else:
                c1.font = data_bold

            c2 = ws.cell(row=curr_r, column=2, value=st_qty)
            c2.font = data_bold
            c2.alignment = center_align
            c2.border = cell_border

            c3 = ws.cell(row=curr_r, column=3, value=st_def)
            c3.font = data_font
            c3.alignment = left_align
            c3.border = cell_border
            curr_r += 1

        # 4. PHẦN 3: BẢNG CHI TIẾT TEST CASE
        curr_r += 2
        ws.cell(row=curr_r, column=1, value=f"PHẦN 3: BẢNG CHI TIẾT TEST CASE ({uc_id}: {uc_name})").font = section_font
        curr_r += 1

        tc_headers = [
            "ID test case", 
            "Mục đích kiểm thử", 
            "Kỹ thuật áp dụng", 
            "Dữ liệu đầu vào", 
            "Các bước thực hiện", 
            "Kết quả mong đợi", 
            "Kết quả thực tế", 
            "Trạng thái (Pass/Fail/N/A)", 
            "Ghi chú"
        ]
        ws.row_dimensions[curr_r].height = 26
        for c_idx, h_text in enumerate(tc_headers, 1):
            cell = ws.cell(row=curr_r, column=c_idx, value=h_text)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center_align
            cell.border = header_border

        tc_start_row = curr_r + 1
        for tc in test_cases:
            tc_id, tc_obj, tc_tech, tc_inp, tc_steps, tc_exp, tc_act, tc_status, tc_note = tc
            ws.row_dimensions[tc_start_row].height = 42 if len(tc_note) > 70 or len(tc_steps) > 80 else 26

            c1 = ws.cell(row=tc_start_row, column=1, value=tc_id)
            c1.font = data_bold
            c1.alignment = center_align
            c1.border = cell_border

            c2 = ws.cell(row=tc_start_row, column=2, value=tc_obj)
            c2.font = data_font
            c2.alignment = wrap_left_align
            c2.border = cell_border

            c3 = ws.cell(row=tc_start_row, column=3, value=tc_tech)
            c3.font = data_font
            c3.alignment = wrap_center_align
            c3.border = cell_border

            c4 = ws.cell(row=tc_start_row, column=4, value=tc_inp)
            c4.font = data_font
            c4.alignment = wrap_left_align
            c4.border = cell_border

            c5 = ws.cell(row=tc_start_row, column=5, value=tc_steps)
            c5.font = data_font
            c5.alignment = wrap_left_align
            c5.border = cell_border

            c6 = ws.cell(row=tc_start_row, column=6, value=tc_exp)
            c6.font = data_font
            c6.alignment = wrap_left_align
            c6.border = cell_border

            c7 = ws.cell(row=tc_start_row, column=7, value=tc_act)
            c7.font = data_font
            c7.alignment = wrap_left_align
            c7.border = cell_border

            c8 = ws.cell(row=tc_start_row, column=8, value=tc_status)
            c8.alignment = center_align
            c8.border = cell_border
            if tc_status == "Pass":
                c8.font = pass_font
                c8.fill = pass_fill
            elif tc_status == "Fail":
                c8.font = fail_font
                c8.fill = fail_fill
            else:
                c8.font = na_font
                c8.fill = na_fill

            c9 = ws.cell(row=tc_start_row, column=9, value=tc_note)
            c9.font = data_font
            c9.alignment = wrap_left_align
            c9.border = cell_border

            tc_start_row += 1

        # 5. PHẦN 4: KẾT LUẬN & THẢO LUẬN (DISCUSSION)
        curr_r = tc_start_row + 1
        ws.cell(row=curr_r, column=1, value="PHẦN 4: NHẬN ĐỊNH & KIẾN NGHỊ KHẮC PHỤC (DISCUSSION)").font = section_font
        curr_r += 1

        ws.row_dimensions[curr_r].height = 22
        ws.cell(row=curr_r, column=1, value="Conclusion:").font = meta_label_font
        ws.cell(row=curr_r, column=2, value=conclusion).font = data_bold
        curr_r += 1

        ws.row_dimensions[curr_r].height = 22
        ws.cell(row=curr_r, column=1, value="Discussion:").font = meta_label_font
        ws.cell(row=curr_r, column=2, value=discussions[0]).font = disc_font

        for d_line in discussions[1:]:
            curr_r += 1
            ws.row_dimensions[curr_r].height = 20
            ws.cell(row=curr_r, column=2, value=d_line).font = disc_font

        # Column widths
        ws.column_dimensions["A"].width = 14
        ws.column_dimensions["B"].width = 30
        ws.column_dimensions["C"].width = 22
        ws.column_dimensions["D"].width = 30
        ws.column_dimensions["E"].width = 38
        ws.column_dimensions["F"].width = 38
        ws.column_dimensions["G"].width = 38
        ws.column_dimensions["H"].width = 15
        ws.column_dimensions["I"].width = 35

    # =========================================================================
    # DATA FOR SHEET 1: ST_Register (UC02: Registration)
    # =========================================================================
    reg_stats = {
        "tested": 18,
        "pass": 11,
        "fail": 7,
        "na": 0,
        "general_comment": "Hệ thống đã triển khai được luồng đăng ký tài khoản khách hàng hoàn chỉnh kèm cơ chế xác thực mã OTP 6 số qua email. Tuy nhiên, tồn tại sự sai lệch lớn giữa tài liệu đặc tả Luận văn và mã nguồn thực tế; cơ chế gửi email qua Redis Pub/Sub tiềm ẩn nguy cơ mất mát dữ liệu; thông báo Joi validation chưa được Việt hóa.",
        "general_info": "Kiểm thử mức hệ thống (System Testing) kết hợp Black-box testing giao diện ReactJS, kiểm thử API Gateway, auth-service, Redis cache OTP và PostgreSQL tblUser."
    }
    reg_eval = {
        "content": "Kiểm thử hệ thống toàn diện cho chức năng Đăng ký tài khoản (UC02: Registration) và luồng Xác thực mã OTP (OTP Verification Flow)"
    }
    reg_conclusion = "Conditionally Approved (TỪ CHỐI PHÊ DUYỆT BÀN GIAO - YÊU CẦU BẮT BUỘC SỬA CODE & CẬP NHẬT ĐẶC TẢ)"
    reg_discussions = [
        "1. Điểm mạnh: Luồng đăng ký khách hàng hoạt động tương đối trơn tru từ form nhập liệu đến giao diện nhập OTP. Mật khẩu được mã hóa an toàn bằng thuật toán bcrypt với 10 salt rounds. Mã OTP được quản lý với TTL 300 giây và tự động khóa sau 5 lần nhập sai.",
        "2. Vấn đề phát hiện nghiêm trọng: Sai lệch đặc tả tài liệu (Luận văn Bảng 2 mục 5b ghi lỗi 'Tài khoản/mật khẩu không chính xác' khi trùng email do lỗi copy-paste từ Login). Joi validation trả về lỗi tiếng Anh thô kệch trên giao diện nếu vượt qua client-side check. Cơ chế gửi OTP qua Redis Pub/Sub là fire-and-forget, không bền vững, dễ làm mất email nếu service restart.",
        "3. Rủi ro lớn: Thiếu cơ chế Rate Limit khi người dùng spam nút 'Gửi lại mã OTP'; thiếu xử lý trim() khoảng trắng khiến người dùng vô tình copy thừa space bị từ chối đăng ký vô lý. Cần sửa code và cập nhật lại Bảng đặc tả 2 trong luận văn trước khi bảo vệ tốt nghiệp."
    ]

    reg_test_cases = [
        (
            "TC_REG_01",
            "Kiểm tra đăng ký thành công với đầy đủ thông tin hợp lệ (Happy Path)",
            "Phân vùng tương đương (EP)",
            "Email: 'newuser1@gmail.com', Pass: 'Pass123@', ConfirmPass: 'Pass123@', Họ: 'Nguyễn', Tên: 'Văn A', Địa chỉ: 'Hà Nội'",
            "1. Truy cập trang /register.\n2. Nhập đầy đủ thông tin hợp lệ vào form.\n3. Nhấn nút 'ĐĂNG KÝ'.",
            "Hệ thống tạo user ở trạng thái PENDING, sinh mã OTP 6 số lưu vào Redis (TTL 300s), gửi email xác thực và tự động chuyển sang trang /verify.",
            "Tạo thành công user PENDING trong PostgreSQL, mã OTP lưu Redis, Frontend hiển thị thông báo thành công và chuyển hướng sang trang /verify?email=newuser1@gmail.com.",
            "Pass",
            "Luồng đăng ký cơ bản (Happy path) hoạt động chính xác."
        ),
        (
            "TC_REG_02",
            "Kiểm tra xác thực mã OTP thành công sau khi đăng ký (Happy Path)",
            "Kiểm thử chuyển trạng thái (ST)",
            "Email: 'newuser1@gmail.com', OTP: Nhập chính xác 6 số OTP lấy từ Redis",
            "1. Tại trang /verify, nhập đúng 6 số OTP.\n2. Nhấn nút 'Xác nhận OTP'.",
            "Hệ thống kiểm tra khớp OTP, kích hoạt user sang trạng thái ACTIVE, xóa key OTP trong Redis và điều hướng sang trang /login.",
            "Tài khoản chuyển sang ACTIVE trong CSDL, xóa OTP cache, thông báo 'OTP đã được xác thực thành công' và chuyển về /login.",
            "Pass",
            "Luồng xác thực OTP và kích hoạt tài khoản hoạt động tốt."
        ),
        (
            "TC_REG_03",
            "Kiểm tra để trống trường Email",
            "Phân tích giá trị biên (BVA)",
            "Email: '', Pass: 'Pass123@', ConfirmPass: 'Pass123@', Họ: 'Nguyễn', Tên: 'An'",
            "1. Nhập đầy đủ các trường, để trống ô Email.\n2. Nhấn nút 'ĐĂNG KÝ'.",
            "Theo Đặc tả Luận văn Bảng 2 (5a): Hệ thống hiển thị thông báo lỗi 'Vui lòng điền đầy đủ thông tin'.",
            "Bị chặn bởi HTML5 tooltip của trình duyệt. Khi gọi API trực tiếp, Joi trả về lỗi tiếng Anh: '\"email\" is required'.",
            "Fail",
            "LỆCH ĐẶC TẢ: Không hiển thị thông báo tiếng Việt theo chuẩn đặc tả Exception 5a; thông điệp Joi chưa được Việt hóa."
        ),
        (
            "TC_REG_04",
            "Kiểm tra để trống trường Mật khẩu",
            "Phân tích giá trị biên (BVA)",
            "Email: 'testpass@gmail.com', Pass: '', ConfirmPass: '', Họ: 'Trần', Tên: 'Bình'",
            "1. Nhập đầy đủ, để trống ô Mật khẩu.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống thông báo lỗi: 'Vui lòng điền đầy đủ thông tin'.",
            "Bị chặn bởi HTML5 input. Khi gọi API, Joi trả lỗi tiếng Anh: '\"password\" is required'.",
            "Fail",
            "LỆCH ĐẶC TẢ: Lỗi thông điệp ngoại lệ 5a chưa được nội địa hóa."
        ),
        (
            "TC_REG_05",
            "Kiểm tra để trống trường Họ hoặc Tên",
            "Phân tích giá trị biên (BVA)",
            "Email: 'testname@gmail.com', Pass: 'Pass123@', ConfirmPass: 'Pass123@', Họ: '', Tên: ''",
            "1. Để trống ô Họ và Tên.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống yêu cầu nhập đầy đủ Họ và Tên người dùng.",
            "Bị chặn bởi HTML5 required. Khi gọi API, Joi trả về lỗi: '\"firstName\" is not allowed to be empty'.",
            "Fail",
            "Thông báo lỗi trả về từ Backend chưa được Việt hóa thân thiện."
        ),
        (
            "TC_REG_06",
            "Kiểm tra đăng ký với Email đã tồn tại trong CSDL",
            "Phân vùng tương đương (EP)",
            "Email: 'customer@cinema.com' (đã tồn tại), Pass: 'Pass123@', ConfirmPass: 'Pass123@', Họ: 'Lê', Tên: 'C'",
            "1. Nhập Email đã tồn tại trên hệ thống.\n2. Nhập các thông tin khác hợp lệ.\n3. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống từ chối và thông báo rõ: 'Email đã tồn tại trong hệ thống'.",
            "Backend trả về mã 400 kèm message: 'Email đã tồn tại trong hệ thống'.",
            "Fail",
            "LỆCH ĐẶC TẢ NGHIÊM TRỌNG: Code chạy đúng logic ('Email đã tồn tại'), nhưng Luận văn Bảng 2 mục 5b lại ghi đặc tả là: 'Tài khoản/mật khẩu không chính xác' (lỗi tài liệu luận văn copy nhầm từ Login)."
        ),
        (
            "TC_REG_07",
            "Kiểm tra Mật khẩu có độ dài dưới 6 ký tự (5 ký tự - Giá trị biên)",
            "Phân tích giá trị biên (BVA)",
            "Email: 'shortpass@gmail.com', Pass: '12345', ConfirmPass: '12345', Họ: 'Phạm', Tên: 'D'",
            "1. Nhập mật khẩu 5 ký tự.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống báo lỗi yêu cầu mật khẩu phải có tối thiểu 6 ký tự.",
            "Backend Joi chặn với lỗi tiếng Anh: '\"password\" length must be at least 6 characters long'.",
            "Fail",
            "Bắt đúng lỗi biên nhưng thông báo lỗi chưa được Việt hóa trên giao diện."
        ),
        (
            "TC_REG_08",
            "Kiểm tra Mật khẩu đạt đúng độ dài biên tối thiểu (6 ký tự)",
            "Phân tích giá trị biên (BVA)",
            "Email: 'exact6pass@gmail.com', Pass: '123456', ConfirmPass: '123456', Họ: 'Vũ', Tên: 'E'",
            "1. Nhập mật khẩu đúng 6 ký tự.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống chấp nhận mật khẩu 6 ký tự và tiến hành gửi mã OTP xác thực.",
            "Đăng ký thành công, tạo user PENDING và chuyển sang trang /verify.",
            "Pass",
            "Kiểm tra giá trị biên dưới hợp lệ (Boundary Valid = 6) hoạt động chính xác."
        ),
        (
            "TC_REG_09",
            "Kiểm tra Xác nhận mật khẩu không trùng khớp với Mật khẩu",
            "Bảng quyết định (DT)",
            "Email: 'mismatch@gmail.com', Pass: 'Password123', ConfirmPass: 'DifferentPass456', Họ: 'Đỗ', Tên: 'F'",
            "1. Nhập Mật khẩu và Xác nhận mật khẩu khác nhau.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống cảnh báo hai mật khẩu không khớp nhau, không cho gửi request.",
            "Backend Joi chặn với lỗi: '\"confirmPassword\" must be [ref:password]'.",
            "Fail",
            "Phát hiện lỗi không khớp nhưng thông điệp lỗi kỹ thuật tiếng Anh gây khó hiểu cho người dùng."
        ),
        (
            "TC_REG_10",
            "Kiểm tra nhập Email không đúng định dạng (thiếu @, thiếu domain)",
            "Phân vùng tương đương (EP)",
            "Email: 'invalidemail.com' hoặc 'user@', Pass: 'Pass123@', ConfirmPass: 'Pass123@'",
            "1. Nhập email sai định dạng.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống thông báo định dạng email không hợp lệ.",
            "Trình duyệt cảnh báo định dạng email. Khi test qua API, Joi trả về '\"email\" must be a valid email'.",
            "Pass",
            "Xác thực định dạng email chuẩn RFC hoạt động chính xác."
        ),
        (
            "TC_REG_11",
            "Kiểm tra nhập Email có khoảng trắng thừa ở đầu/cuối",
            "Đoán lỗi (Error Guessing)",
            "Email: '  validuser@gmail.com  ', Pass: 'Pass123@', ConfirmPass: 'Pass123@'",
            "1. Nhập email có space ở đầu và cuối.\n2. Nhấn 'ĐĂNG KÝ'.",
            "Hệ thống tự động cắt bỏ khoảng trắng (Trim) và đăng ký bình thường.",
            "Joi schema không cấu hình .trim(), coi khoảng trắng là ký tự của email nên báo lỗi email không hợp lệ.",
            "Fail",
            "THIẾU SÓT: Thiếu hàm trim() chuẩn hóa dữ liệu đầu vào."
        ),
        (
            "TC_REG_12",
            "Kiểm tra nhập sai mã OTP lần đầu tại trang xác thực",
            "Phân vùng tương đương (EP)",
            "Email: 'user_otp@gmail.com', OTP: '000000' (mã sai)",
            "1. Tại trang /verify, nhập mã OTP sai.\n2. Nhấn 'Xác nhận OTP'.",
            "Theo Luận văn Bảng 2 mục 8: Hệ thống thông báo 'Mã xác nhận không chính xác' và hiển thị số lần thử còn lại.",
            "Hệ thống hiển thị thông báo: 'Invalid OTP. 4 attempts remaining.' và tăng biến đếm count trong Redis.",
            "Pass",
            "Bắt đúng mã OTP sai và quản lý số lần thử còn lại chính xác."
        ),
        (
            "TC_REG_13",
            "Kiểm tra nhập sai mã OTP liên tiếp 5 lần (Giá trị biên Max Attempts)",
            "Kiểm thử chuyển trạng thái & Biên",
            "Email: 'user_otp@gmail.com', Thử sai mã OTP lần thứ 5 và thứ 6",
            "1. Nhập sai mã OTP liên tiếp 5 lần.\n2. Thử nhập lần thứ 6.",
            "Hệ thống khóa xác thực và thông báo: 'Bạn đã nhập sai OTP quá nhiều lần. Vui lòng thử lại sau'.",
            "Đến lần thứ 5, hệ thống từ chối và trả về ErrorMessages.OTP_MAX_ATTEMPTS: 'Bạn đã nhập sai OTP quá nhiều lần. Vui lòng thử lại sau'.",
            "Pass",
            "Cơ chế chống Brute-force OTP hoạt động rất tốt và an toàn."
        ),
        (
            "TC_REG_14",
            "Kiểm tra xác thực với mã OTP đã hết hạn (Sau 300 giây / 5 phút)",
            "Kiểm thử theo thời gian (Time-out)",
            "Email: 'user_otp@gmail.com', Chờ sau 5 phút và nhập mã OTP cũ",
            "1. Nhận mã OTP nhưng không nhập ngay.\n2. Chờ 5 phút (TTL Redis = 300s).\n3. Nhập mã OTP và xác nhận.",
            "Hệ thống từ chối và thông báo: 'Mã OTP đã hết hạn'.",
            "Redis tự động xóa key otp:email sau 300s; hệ thống trả về ErrorMessages.OTP_EXPIRED: 'Mã OTP đã hết hạn'.",
            "Pass",
            "Quản lý vòng đời TTL của OTP trên Redis hoạt động chuẩn xác."
        ),
        (
            "TC_REG_15",
            "Kiểm tra nhập mã OTP không đủ 6 chữ số hoặc chứa chữ cái",
            "Phân tích giá trị biên (BVA)",
            "Email: 'user_otp@gmail.com', OTP: '123' hoặc '12ab56'",
            "1. Nhập mã OTP có độ dài 3 ký tự hoặc chứa chữ.\n2. Nhấn 'Xác nhận OTP'.",
            "Hệ thống chặn không cho gửi hoặc thông báo mã OTP phải gồm đúng 6 chữ số.",
            "verifyOtpSchema của Joi chặn với lỗi: '\"otp\" length must be 6 characters long'.",
            "Pass",
            "Đảm bảo toàn vẹn định dạng mã OTP 6 số."
        ),
        (
            "TC_REG_16",
            "Kiểm tra tính năng gửi lại mã OTP (Resend OTP)",
            "Kiểm thử chức năng (Functional)",
            "Email: 'user_otp@gmail.com', Nhấn nút 'Gửi lại mã OTP'",
            "1. Tại trang /verify, click vào nút 'Gửi lại mã OTP'.",
            "Hệ thống sinh mã OTP mới, ghi đè vào Redis, gửi lại email và giới hạn tần suất gửi (Rate limit ít nhất 60s/lần).",
            "Hệ thống sinh OTP mới thành công nhưng KHÔNG CÓ Rate Limiting thời gian chờ 60 giây, người dùng có thể spam click liên tục gây nghẽn email.",
            "Fail",
            "RỦI RO BẢO MẬT & TÀI NGUYÊN: Thiếu cơ chế Cooldown / Rate Limiting 60s cho chức năng gửi lại OTP."
        ),
        (
            "TC_REG_17",
            "Kiểm tra tính toàn vẹn sự kiện OTP khi Redis Pub/Sub gặp sự cố",
            "Kiểm thử độ tin cậy (Reliability / McCall)",
            "Giả lập Redis Pub/Sub bị ngắt kết nối hoặc worker email bận",
            "1. Gửi request đăng ký tài khoản.\n2. Quan sát hàng đợi sự kiện và trạng thái tài khoản.",
            "Sự kiện gửi email OTP phải được lưu trữ bền vững (Transactional Outbox) và có cơ chế thử lại (Retry) nếu gửi lỗi.",
            "Sử dụng redisPubSubClient.publish là cơ chế bắn-bỏ (fire-and-forget), nếu worker không nhận được thì thông điệp mất vĩnh viễn, user bị kẹt ở PENDING mà không thể tự kích hoạt.",
            "Fail",
            "LỖI THIẾT KẾ KIẾN TRÚC: Không áp dụng Transactional Outbox Pattern cho sự kiện xác thực email như đã áp dụng cho Booking."
        ),
        (
            "TC_REG_18",
            "Kiểm tra tính năng Ẩn/Hiện mật khẩu và Xác nhận mật khẩu",
            "Kiểm thử giao diện (UI Testing)",
            "Mật khẩu: 'SecretPass123'",
            "1. Nhập mật khẩu.\n2. Click icon con mắt ở cả 2 ô Mật khẩu và Xác nhận mật khẩu.",
            "Chuyển đổi qua lại mượt mà giữa dạng ẩn (password) và dạng hiển thị rõ (text).",
            "Giao diện toggle state showPassword và showConfirmPassword mượt mà, chuyển đổi đúng kiểu input.",
            "Pass",
            "Tính năng trợ năng UI hoạt động tốt."
        )
    ]

    # =========================================================================
    # DATA FOR SHEET 2: ST_EditProfile (UC19: Edit Personal Information)
    # =========================================================================
    prof_stats = {
        "tested": 17,
        "pass": 10,
        "fail": 7,
        "na": 0,
        "general_comment": "Chức năng chỉnh sửa thông tin cá nhân và tích hợp ví Web3 MetaMask đã hoạt động được các nghiệp vụ cơ bản. Tuy nhiên, phát hiện lỗi đồng bộ dữ liệu giao diện nghiêm trọng (tên mới cập nhật thành công nhưng Header và LocalStorage vẫn hiển thị tên cũ); dữ liệu số dư ví tiền điện tử BTC và USDT bị hardcode giả lập; và thông báo giao diện còn dùng hàm alert() thô sơ.",
        "general_info": "Kiểm thử mức hệ thống (System Testing) kết hợp kiểm thử tích hợp giữa Frontend ProfilePage.jsx, user-service, PostgreSQL tblUser, customer_profile và Web3 Ethers.js."
    }
    prof_eval = {
        "content": "Kiểm thử hệ thống toàn diện cho chức năng Xem và Chỉnh sửa thông tin cá nhân (UC19: Edit Personal Information) kết hợp tích hợp ví Web3 on-chain"
    }
    reg_conclusion_prof = "Conditionally Approved (TỪ CHỐI PHÊ DUYỆT BÀN GIAO - BẮT BUỘC SỬA LỖI ĐỒNG BỘ DỮ LIỆU & HARDCODE)"
    prof_discussions = [
        "1. Điểm mạnh: Trang hồ sơ cá nhân hiển thị đa dạng thông tin: thông tin định danh, địa chỉ ví on-chain, lịch sử đặt vé gần nhất; tích hợp thư viện Ethers.js kết nối ví MetaMask trực quan và kiểm soát phân quyền sửa thông tin theo đúng user_id của tài khoản đăng nhập.",
        "2. Vấn đề phát hiện nghiêm trọng: Phát hiện BUG ĐỒNG BỘ GIAO DIỆN: Sau khi cập nhật tên mới thành công, hệ thống không cập nhật lại object user trong localStorage, dẫn đến thanh điều hướng Header vẫn hiển thị tên cũ cho đến khi đăng xuất đăng nhập lại. Dữ liệu số dư ví BTC ('0.01') và USDT ('1000') bị gán cứng giả lập (Fake hardcoded data).",
        "3. Rủi ro lớn: Thiếu kiểm tra ràng buộc định dạng số điện thoại ở Frontend; việc ẩn/chặn đổi Email chưa có giải thích rõ ràng gây hiểu lầm cho người dùng. Cần sửa triệt để các lỗi này để đáp ứng yêu cầu thẩm định phần mềm."
    ]

    prof_test_cases = [
        (
            "TC_PROF_01",
            "Kiểm tra tải và hiển thị thông tin cá nhân hiện tại (Happy Path)",
            "Phân vùng tương đương (EP)",
            "User đã đăng nhập: id = 'cust_01', Name: 'Nguyễn Văn A', Email: 'customer@cinema.com'",
            "1. Đăng nhập vào hệ thống.\n2. Điều hướng vào trang Profile (/profile).\n3. Quan sát thông tin hiển thị.",
            "Hệ thống gọi API getUserById, hiển thị chính xác họ tên, email, số điện thoại, ngày sinh, địa chỉ và lịch sử đặt vé.",
            "Dữ liệu tải chính xác từ CSDL PostgreSQL, hiển thị đầy đủ thông tin cá nhân và danh sách vé đã đặt.",
            "Pass",
            "Luồng tải thông tin hồ sơ cá nhân hoạt động tốt."
        ),
        (
            "TC_PROF_02",
            "Kiểm tra cập nhật thành công thông tin cá nhân với dữ liệu hợp lệ (Happy Path)",
            "Phân vùng tương đương (EP)",
            "Tên mới: 'Nguyễn Văn An Cập Nhật', SĐT: '0987654321', Ngày sinh: '1995-05-20', Địa chỉ: '456 Đường Cầu Giấy, Hà Nội'",
            "1. Nhấn nút 'Chỉnh sửa' (icon cây bút).\n2. Nhập các thông tin mới hợp lệ.\n3. Nhấn 'Lưu thay đổi'.",
            "Theo Luận văn Bảng 19: Hệ thống cập nhật thông tin vào CSDL, đóng form sửa và hiển thị thông báo cập nhật thành công.",
            "API updateUser trả về success: true, thông tin trên trang Profile được cập nhật sang dữ liệu mới.",
            "Pass",
            "Cập nhật thông tin vào CSDL PostgreSQL thành công."
        ),
        (
            "TC_PROF_03",
            "Kiểm tra để trống trường Họ và Tên khi cập nhật",
            "Phân tích giá trị biên (BVA)",
            "Tên mới: '' (chuỗi rỗng), SĐT: '0987654321'",
            "1. Bật chế độ chỉnh sửa.\n2. Xóa trắng trường Họ và Tên.\n3. Nhấn 'Lưu thay đổi'.",
            "Theo Luận văn Bảng 19 mục 4: Hệ thống thông báo lỗi: 'Vui lòng nhập đầy đủ thông tin cá nhân'.",
            "Giao diện không validate required cho trường Tên, gửi request chuỗi rỗng xuống backend, backend lưu tên rỗng hoặc báo lỗi chung không thân thiện.",
            "Fail",
            "LỆCH ĐẶC TẢ: Thiếu kiểm tra trường bắt buộc ở Client; không hiển thị đúng thông báo lỗi theo Exception 4 của Luận văn."
        ),
        (
            "TC_PROF_04",
            "Kiểm tra nhập Số điện thoại chứa chữ cái hoặc ký tự đặc biệt",
            "Phân vùng tương đương (EP)",
            "SĐT: '0987abcxyz' hoặc '098-@#$'",
            "1. Nhập số điện thoại chứa chữ cái.\n2. Nhấn 'Lưu thay đổi'.",
            "Hệ thống từ chối và thông báo số điện thoại không đúng định dạng.",
            "Frontend không kiểm tra regex số điện thoại, gửi thẳng dữ liệu rác xuống CSDL.",
            "Fail",
            "THIẾU SÓT: Thiếu regex validate định dạng số điện thoại Việt Nam (10 chữ số bắt đầu bằng 0)."
        ),
        (
            "TC_PROF_05",
            "Kiểm tra chọn Ngày sinh trong tương lai (Invalid Date)",
            "Phân tích giá trị biên (BVA)",
            "Ngày sinh: '2030-12-31' (ngày trong tương lai)",
            "1. Chọn ngày sinh là một ngày lớn hơn ngày hiện tại.\n2. Nhấn 'Lưu thay đổi'.",
            "Hệ thống chặn và thông báo ngày sinh không thể là ngày trong tương lai.",
            "Input date không có thuộc tính max={today}, hệ thống cho phép lưu ngày sinh năm 2030 vào cơ sở dữ liệu.",
            "Fail",
            "LỖI LOGIC DỮ LIỆU: Cho phép lưu ngày sinh trong tương lai làm sai lệch thông tin khách hàng."
        ),
        (
            "TC_PROF_06",
            "Kiểm tra cố tình thay đổi địa chỉ Email trên giao diện Profile",
            "Bảng quyết định (DT)",
            "Email sửa thành: 'newemail_change@gmail.com'",
            "1. Mở form chỉnh sửa hồ sơ.\n2. Cố gắng nhập email mới và lưu.",
            "Nếu hệ thống không cho phép đổi email thì phải disable trường email và có tooltip giải thích rõ ràng.",
            "Code ProfilePage.jsx line 156 bóc tách email ra khỏi request (const { email, ...updateData } = editForm), form vẫn cho gõ nhưng khi lưu thì email âm thầm bị bỏ qua mà không có thông báo giải thích cho người dùng.",
            "Fail",
            "LỖI UX: Âm thầm bỏ qua thay đổi email mà không thông báo hoặc disable trường email."
        ),
        (
            "TC_PROF_07",
            "Kiểm tra đồng bộ dữ liệu người dùng trên Header và LocalStorage sau khi đổi tên",
            "Kiểm thử tích hợp hệ thống (Integration)",
            "Tên mới: 'Trần Văn Minh'",
            "1. Cập nhật tên mới thành công.\n2. Quan sát tên hiển thị trên thanh điều hướng (Navbar Header).\n3. Kiểm tra localStorage.getItem('user').",
            "Tên trên Navbar Header phải lập tức cập nhật sang 'Trần Văn Minh' và localStorage cũng phải lưu object user mới.",
            "Header vẫn hiển thị tên cũ 'Nguyễn Văn A' vì code chỉ setUserData trong component ProfilePage mà KHÔNG cập nhật localStorage.setItem('user', ...) và không bắn event cập nhật state toàn cục!",
            "Fail",
            "BUG ĐỒNG BỘ DỮ LIỆU NGHIÊM TRỌNG: Tên mới chỉ đổi trong trang Profile, toàn bộ thanh Header trên website vẫn hiện tên cũ cho đến khi người dùng đăng xuất đăng nhập lại."
        ),
        (
            "TC_PROF_08",
            "Kiểm tra tính chính xác của số dư ví tiền điện tử hiển thị trên Profile",
            "Kiểm thử tính đúng đắn (Correctness)",
            "Kết nối ví MetaMask",
            "1. Kết nối ví MetaMask vào hệ thống.\n2. Quan sát các mục số dư ETH, BTC, USDT hiển thị trên màn hình.",
            "Hệ thống phải hiển thị số dư thực tế từ smart contract hoặc chỉ hiển thị token mạng hỗ trợ (ETH Sepolia).",
            "ProfilePage.jsx lines 118-121 gán cứng số dư giả: BTC: '0.01' và USDT: '1000' (Fake simulated balances), gây hiểu nhầm rằng người dùng có tiền thật.",
            "Fail",
            "DỮ LIỆU GIẢ MẠO (HARDCODED DUMMY DATA): Gán cứng số dư tiền điện tử thay vì truy vấn blockchain thực tế."
        ),
        (
            "TC_PROF_09",
            "Kiểm tra kết nối ví MetaMask thành công và lưu địa chỉ ví vào profile",
            "Kiểm thử chức năng Web3 (Integration)",
            "Ví MetaMask đã cài trên trình duyệt, mạng Sepolia Testnet",
            "1. Nhấn nút 'Kết nối ví MetaMask'.\n2. Phê duyệt kết nối trên extension MetaMask.",
            "Hệ thống lấy được địa chỉ ví (0x...), hiển thị dạng rút gọn (0x12...34) và cập nhật onchain_wallet_address vào customer_profile.",
            "Kết nối thành công qua Ethers.js BrowserProvider, hiển thị đúng địa chỉ ví và số dư ETH.",
            "Pass",
            "Tích hợp Web3 Ethers.js kết nối ví MetaMask hoạt động tốt."
        ),
        (
            "TC_PROF_10",
            "Kiểm tra kết nối ví khi trình duyệt chưa cài extension MetaMask",
            "Đoán lỗi (Error Guessing)",
            "Trình duyệt ẩn danh không cài MetaMask (window.ethereum is undefined)",
            "1. Nhấn nút 'Kết nối ví MetaMask'.",
            "Hệ thống hiển thị popup hướng dẫn người dùng cài đặt extension MetaMask.",
            "Hệ thống bật hộp thoại alert() thô sơ: 'MetaMask chưa được cài đặt. Vui lòng cài đặt MetaMask để tiếp tục.'",
            "Fail",
            "UX KÉM: Sử dụng hàm alert() nguyên thủy của trình duyệt thay vì Toast/Modal component của ứng dụng."
        ),
        (
            "TC_PROF_11",
            "Kiểm tra tính năng ngắt kết nối ví MetaMask",
            "Kiểm thử chuyển trạng thái (ST)",
            "Ví đang ở trạng thái Connected",
            "1. Nhấn nút 'Ngắt kết nối ví'.",
            "Hệ thống xóa địa chỉ ví hiển thị, reset trạng thái walletConnected về false.",
            "Hệ thống reset state ví về rỗng và hiển thị alert 'Đã ngắt kết nối ví'.",
            "Pass",
            "Ngắt kết nối ví hoạt động đúng nghiệp vụ."
        ),
        (
            "TC_PROF_12",
            "Kiểm tra cập nhật trường Địa chỉ với độ dài lớn (Boundary Test)",
            "Phân tích giá trị biên (BVA)",
            "Địa chỉ: Chuỗi văn bản tiếng Việt dài 300 ký tự",
            "1. Nhập địa chỉ dài 300 ký tự.\n2. Nhấn 'Lưu thay đổi'.",
            "Hệ thống lưu thành công địa chỉ mà không bị cắt cụt (truncate) dữ liệu.",
            "Cột address trong tblUser là kiểu TEXT/VARCHAR(255)+ nên lưu trữ trọn vẹn 300 ký tự.",
            "Pass",
            "Xử lý chuỗi văn bản dài trong CSDL tốt."
        ),
        (
            "TC_PROF_13",
            "Kiểm tra lưu trữ ký tự tiếng Việt có dấu Unicode (UTF-8)",
            "Phân vùng tương đương (EP)",
            "Tên: 'Nguyễn Đắc Triệu Khang', Địa chỉ: 'Số 12 ngõ 34 Phố Huế, P. Hàng Bài, Q. Hoàn Kiếm, Hà Nội'",
            "1. Nhập toàn bộ dữ liệu có dấu tiếng Việt phức tạp.\n2. Nhấn 'Lưu thay đổi'.",
            "Hệ thống hiển thị và lưu trữ đúng nguyên vẹn dấu tiếng Việt, không bị lỗi font (phù hiệu lạ ???).",
            "Hệ thống lưu trữ UTF-8 chính xác trong CSDL PostgreSQL, hiển thị chuẩn xác trên giao diện.",
            "Pass",
            "Hỗ trợ bộ ký tự tiếng Việt Unicode hoàn hảo."
        ),
        (
            "TC_PROF_14",
            "Kiểm thử bảo mật IDOR: Người dùng A gọi API sửa thông tin của Người dùng B",
            "Kiểm thử bảo mật (Security - BOLA/IDOR)",
            "Token của User A, gửi PUT /api/v1/users/:id_of_user_B",
            "1. Đăng nhập bằng tài khoản User A lấy Bearer Token.\n2. Gửi request PUT cập nhật thông tin với ID của User B.",
            "Hệ thống từ chối với mã lỗi 403 Forbidden hoặc 401 Unauthorized, không cho phép sửa chéo dữ liệu.",
            "Backend userService.ts kiểm tra requesterId !== targetUserId và requesterRole !== 'admin', ném lỗi và từ chối cập nhật.",
            "Pass",
            "Bảo mật chống tấn công IDOR phân quyền đối tượng hoạt động rất tốt."
        ),
        (
            "TC_PROF_15",
            "Kiểm thử tấn công chèn mã Cross-Site Scripting (XSS) qua Họ tên hoặc Địa chỉ",
            "Kiểm thử bảo mật (Security Testing)",
            "Tên: '<script>alert(document.cookie)</script>'",
            "1. Nhập mã script XSS vào ô Họ tên.\n2. Nhấn Lưu và tải lại trang.",
            "Hệ thống mã hóa ký tự đặc biệt (HTML Entity Encode), không thực thi script.",
            "React tự động escape chuỗi khi render JSX, script chỉ hiển thị dưới dạng văn bản tĩnh an toàn.",
            "Pass",
            "An toàn trước các cuộc tấn công XSS lưu trữ (Stored XSS)."
        ),
        (
            "TC_PROF_16",
            "Kiểm tra nút 'Hủy' (Cancel) khi đang chỉnh sửa form",
            "Kiểm thử chức năng giao diện (UI)",
            "Đang trong chế độ chỉnh sửa, đã thay đổi thông tin nhưng chưa lưu",
            "1. Sửa tên thành 'Tên Tạm Thời'.\n2. Nhấn nút 'Hủy' (icon dấu X).",
            "Form đóng lại, phục hồi lại toàn bộ thông tin ban đầu trước khi sửa.",
            "State isEditing chuyển về false, editForm được khôi phục về dữ liệu ban đầu từ userData.",
            "Pass",
            "Hủy bỏ thao tác chỉnh sửa hoạt động mượt mà."
        ),
        (
            "TC_PROF_17",
            "Kiểm tra tích hợp hiển thị danh sách 'Lịch sử đặt vé gần nhất'",
            "Kiểm thử tích hợp (Integration Testing)",
            "Tài khoản đã có 2 đơn đặt vé trong hệ thống",
            "1. Vào trang Profile.\n2. Quan sát khối 'Đặt vé gần đây' ở góc dưới.",
            "Hiển thị danh sách tối đa 3 vé đã đặt gần nhất (Tên phim, ngày chiếu, số tiền, trạng thái).",
            "Hàm getUserBookings(1, 3) gọi sang booking-service lấy đúng 3 vé mới nhất và render đẹp mắt.",
            "Pass",
            "Tích hợp giữa User Service và Booking Service trên trang Profile hoạt động tốt."
        )
    ]

    # Create both sheets
    ws_reg = wb.create_sheet(title="ST_Register")
    create_sheet(
        ws_reg, 
        "ST_Register", 
        "UC02", 
        "Đăng ký tài khoản (Registration)", 
        "Frontend RegisterPage.jsx, VerifyOtpPage.jsx | Backend auth-service (Register & Verify OTP) | Redis Cache & PostgreSQL", 
        reg_stats, 
        reg_eval, 
        reg_test_cases, 
        reg_conclusion, 
        reg_discussions
    )

    ws_prof = wb.create_sheet(title="ST_EditProfile")
    create_sheet(
        ws_prof, 
        "ST_EditProfile", 
        "UC19", 
        "Chỉnh sửa thông tin cá nhân (Edit Personal Information)", 
        "Frontend ProfilePage.jsx | Backend user-service (User & Customer Profile) | Web3 Ethers.js MetaMask & PostgreSQL", 
        prof_stats, 
        prof_eval, 
        prof_test_cases, 
        reg_conclusion_prof, 
        prof_discussions
    )

    # Remove default sheet
    wb.remove(default_sheet)

    # Save workbook
    target_excel = r"c:\Users\ADMIN\Documents\cinema-project-main\System_Test_Register_EditProfile.xlsx"
    wb.save(target_excel)
    print(f"System test excel file generated successfully at: {target_excel}")

if __name__ == "__main__":
    build_system_test_excel()
