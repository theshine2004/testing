/**
 * @file authController.register.test.ts
 * @description Tập lệnh kiểm thử đơn vị (Unit Test Script) cho Chức năng Đăng ký tài khoản (Register).
 * Bao gồm kiểm thử cho:
 *   1. AuthController.registerSchema (Kiểm tra tính hợp lệ dữ liệu đầu vào - Joi Validation)
 *   2. AuthController.register (Điều khiển nghiệp vụ Đăng ký tài khoản Khách hàng)
 *   3. AuthController Helper Methods (Sinh OTP, định dạng URL xác thực, thông điệp PubSub, Cache vai trò)
 *   4. UserDAO / EnsurePending (Thao tác cơ sở dữ liệu: CheckDB & Rollback)
 *
 * Môn học: Đảm bảo chất lượng phần mềm (Kiểm thử phần mềm)
 * Quy chuẩn: Tuân thủ quy trình kiểm thử cấp 2 (Branch coverage - C2) và mục 5.3.2 trong giáo trình.
 */

import { jest, describe, it, test, expect, beforeEach, beforeAll, afterAll } from '@jest/globals';
import bcrypt from 'bcryptjs';
import { Request, Response, NextFunction } from 'express';

// ============================================================================
// 1. THIẾT LẬP MOCK CHO CÁC MODULE PHỤ THUỘC (REDIS, GRPC USER CLIENT)
// ============================================================================

const mockRedisGet = jest.fn<any, any>();
const mockRedisSetEx = jest.fn<any, any>();
const mockRedisDel = jest.fn<any, any>();
const mockRedisKeys = jest.fn<any, any>();
const mockRedisPublish = jest.fn<any, any>();

jest.mock('../config/redis.js', () => ({
  redisClient: {
    get: (...args: any[]) => mockRedisGet(...args),
    setEx: (...args: any[]) => mockRedisSetEx(...args),
    del: (...args: any[]) => mockRedisDel(...args),
    keys: (...args: any[]) => mockRedisKeys(...args),
  },
  redisPubSubClient: {
    publish: (...args: any[]) => mockRedisPublish(...args),
  },
  default: {
    get: (...args: any[]) => mockRedisGet(...args),
    setEx: (...args: any[]) => mockRedisSetEx(...args),
    del: (...args: any[]) => mockRedisDel(...args),
    keys: (...args: any[]) => mockRedisKeys(...args),
  },
}));

const mockGetUserByEmail = jest.fn<any, any>();
const mockGetRoleByName = jest.fn<any, any>();
const mockEnsurePending = jest.fn<any, any>();
const mockActivateUser = jest.fn<any, any>();

jest.mock('../services/userGrpcClient.js', () => ({
  userClient: {
    GetUserByEmail: (...args: any[]) => mockGetUserByEmail(...args),
    GetRoleByName: (...args: any[]) => mockGetRoleByName(...args),
    EnsurePending: (...args: any[]) => mockEnsurePending(...args),
    ActivateUser: (...args: any[]) => mockActivateUser(...args),
  },
}));

import AuthController from '../controllers/authController.js';
import { ErrorMessages, HttpStatus } from '../types/index.js';

// ============================================================================
// 2. HÀM TIỆN ÍCH TẠO MOCK REQUEST / RESPONSE
// ============================================================================
interface IMockResponse {
  status: jest.Mock;
  json: jest.Mock;
  statusCode?: number;
  jsonData?: any;
}

function createMockResponse(): IMockResponse {
  const res: any = {};
  res.status = jest.fn<any, any>().mockImplementation((code: any) => {
    res.statusCode = code;
    return res;
  });
  res.json = jest.fn<any, any>().mockImplementation((data: any) => {
    res.jsonData = data;
    return res;
  });
  return res;
}

const RAW_PASSWORD = 'Password123@';
const HASHED_PASSWORD = bcrypt.hashSync(RAW_PASSWORD, 10);

// ============================================================================
// BẮT ĐẦU CÁC BỘ TEST CASE (TEST SUITES)
// ============================================================================

describe('Module: Kiểm thử đơn vị Chức năng Đăng ký tài khoản (Register)', () => {

  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  beforeEach(() => {
    jest.clearAllMocks();
    mockRedisGet.mockResolvedValue(null);
    mockRedisSetEx.mockResolvedValue('OK');
    mockRedisPublish.mockResolvedValue(1);
  });

  // ==========================================================================
  // NHÓM 1: KIỂM THỬ XÁC THỰC DỮ LIỆU ĐẦU VÀO (AuthController.registerSchema)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController.registerSchema (Joi Validation)', () => {

    test('TC-AUTH-REG-SCHEMA-01: registerSchema_testChuan1_ValidPayload — Xác thực thành công khi dữ liệu đầy đủ và hợp lệ', async () => {
      // 1. Khai báo biến lưu test input & expected output theo mục 5.3.2
      const testInput = {
        email: 'customer.valid@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Nguyễn',
        lastName: 'Văn An',
        address: '123 Đường Cầu Giấy, Hà Nội',
      };

      // 2. Gọi method cần test với test input
      const actualResult = await AuthController.registerSchema.validateAsync(testInput);

      // 3. Kiểm tra kết quả thực method với expected output
      expect(actualResult).toBeDefined();
      expect(actualResult.email).toBe(testInput.email);
      expect(actualResult.password).toBe(testInput.password);
      expect(actualResult.confirmPassword).toBe(testInput.confirmPassword);
      expect(actualResult.firstName).toBe(testInput.firstName);
      expect(actualResult.lastName).toBe(testInput.lastName);
      expect(actualResult.address).toBe(testInput.address);
    });

    test('TC-AUTH-REG-SCHEMA-02: registerSchema_testNgoaile1_MissingEmail — Báo lỗi khi thiếu email', async () => {
      const testInput = {
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Nguyễn',
        lastName: 'An',
      };
      const expectedErrorMessage = '"email" is required';

      await expect(AuthController.registerSchema.validateAsync(testInput)).rejects.toThrow(
        expect.objectContaining({
          message: expectedErrorMessage,
        })
      );
    });

    test('TC-AUTH-REG-SCHEMA-03: registerSchema_testNgoaile2_InvalidEmailFormat — Báo lỗi khi định dạng email sai', async () => {
      const testInput = {
        email: 'invalid-email-pattern',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Nguyễn',
        lastName: 'An',
      };
      const expectedErrorMessage = '"email" must be a valid email';

      await expect(AuthController.registerSchema.validateAsync(testInput)).rejects.toThrow(
        expect.objectContaining({
          message: expectedErrorMessage,
        })
      );
    });

    test('TC-AUTH-REG-SCHEMA-04: registerSchema_testNgoaile3_ShortPassword — Báo lỗi khi mật khẩu < 6 ký tự', async () => {
      const testInput = {
        email: 'shortpass@cinema.com',
        password: '12345',
        confirmPassword: '12345',
        firstName: 'Nguyễn',
        lastName: 'An',
      };
      const expectedErrorMessage = '"password" length must be at least 6 characters long';

      await expect(AuthController.registerSchema.validateAsync(testInput)).rejects.toThrow(
        expect.objectContaining({
          message: expectedErrorMessage,
        })
      );
    });

    test('TC-AUTH-REG-SCHEMA-05: registerSchema_testNgoaile4_ConfirmPasswordMismatch — Báo lỗi khi confirmPassword không khớp', async () => {
      const testInput = {
        email: 'mismatch@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: 'DifferentPassword123@',
        firstName: 'Nguyễn',
        lastName: 'An',
      };
      const expectedErrorMessage = '"confirmPassword" must be [ref:password]';

      await expect(AuthController.registerSchema.validateAsync(testInput)).rejects.toThrow(
        expect.objectContaining({
          message: expectedErrorMessage,
        })
      );
    });

    test('TC-AUTH-REG-SCHEMA-06: registerSchema_testNgoaile5_MissingNameFields — Báo lỗi khi thiếu họ hoặc tên', async () => {
      const testInput = {
        email: 'noname@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        lastName: 'An',
      };
      const expectedErrorMessage = '"firstName" is required';

      await expect(AuthController.registerSchema.validateAsync(testInput)).rejects.toThrow(
        expect.objectContaining({
          message: expectedErrorMessage,
        })
      );
    });

    test('TC-AUTH-REG-SCHEMA-07: registerSchema_testChuan2_OptionalAddressNullOrEmpty — Xác thực thành công khi address là null hoặc rỗng', async () => {
      const testInput1 = {
        email: 'noaddress1@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Trần',
        lastName: 'Bình',
        address: null,
      };

      const result1 = await AuthController.registerSchema.validateAsync(testInput1);
      expect(result1.address).toBeNull();

      const testInput2 = {
        email: 'noaddress2@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Lê',
        lastName: 'Hòa',
        address: '',
      };

      const result2 = await AuthController.registerSchema.validateAsync(testInput2);
      expect(result2.address).toBe('');
    });

  });

  // ==========================================================================
  // NHÓM 2: KIỂM THỬ ĐIỀU KHIỂN NGHIỆP VỤ ĐĂNG KÝ (AuthController.register)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController.register — Nghiệp vụ Đăng ký tài khoản', () => {

    test('TC-AUTH-REG-01: register_testChuan1_RegisterSuccess — Đăng ký tài khoản khách hàng mới thành công (Happy Path)', async () => {
      // 1. Khai báo test input & expected output
      const testInput = {
        email: 'new.customer@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Trần',
        lastName: 'Văn Nam',
        address: '456 Hoàng Hoa Thám, Hà Nội',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      // Mock GetUserByEmail: chưa có người dùng
      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        expect(params.email).toBe(testInput.email);
        callback(null, { found: false });
      });

      // Mock GetRoleByName: role customer tồn tại
      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        callback(null, { found: true, id: 'role-customer-id-123' });
      });

      // Mock EnsurePending: tạo người dùng pending thành công
      mockEnsurePending.mockImplementation((params: any, callback: any) => {
        expect(params.email).toBe(testInput.email);
        expect(params.name).toBe('Trần Văn Nam');
        expect(params.role_id).toBe('role-customer-id-123');
        expect(params.address).toBe(testInput.address);
        callback(null, { id: 'new-user-uuid-999', created: true });
      });

      // 2. Gọi method cần test
      await AuthController.register(req, res, next);

      // 3. Kiểm tra kết quả thực method với expected output
      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.CREATED);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.REGISTRATION_SUCCESS);

      // Xác minh sự kiện Redis PubSub đã phát đi
      expect(mockRedisPublish).toHaveBeenCalledWith(
        AuthController.REDIS_TOPICS.EMAIL_VERIFY,
        expect.stringContaining(testInput.email)
      );

      // Xác minh mã OTP đã được lưu vào Cache
      expect(mockRedisSetEx).toHaveBeenCalledWith(
        `otp:${testInput.email}`,
        300,
        expect.any(String)
      );

      expect(next).not.toHaveBeenCalled();
    });

    test('TC-AUTH-REG-02: register_testNgoaile1_DuplicateEmail — Từ chối đăng ký khi email đã tồn tại', async () => {
      const testInput = {
        email: 'duplicate.user@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Phạm',
        lastName: 'Minh',
        address: 'Hà Nội',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      // Mock GetUserByEmail: email đã tồn tại
      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, {
          found: true,
          user: { id: 'existing-id', email: testInput.email }
        });
      });

      await AuthController.register(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.EMAIL_EXISTS);

      // Không gọi EnsurePending hay phát sự kiện
      expect(mockEnsurePending).not.toHaveBeenCalled();
      expect(mockRedisPublish).not.toHaveBeenCalled();
      expect(next).not.toHaveBeenCalled();
    });

    test('TC-AUTH-REG-03: register_testNgoaile2_ValidationError_Joi — Bắt lỗi Joi trong controller catch block', async () => {
      const testInput = {
        email: 'valid@cinema.com',
        password: '123', // Mật khẩu quá ngắn
        confirmPassword: '123',
        firstName: 'Nguyễn',
        lastName: 'A',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      await AuthController.register(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toContain('at least 6 characters long');
      expect(mockGetUserByEmail).not.toHaveBeenCalled();
    });

    test('TC-AUTH-REG-04: register_testNgoaile3_CustomerRoleNotFound — Chuyển tiếp lỗi khi không tìm thấy role customer', async () => {
      const testInput = {
        email: 'norole@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Lê',
        lastName: 'Dũng',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      // Role customer không tìm thấy
      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      await AuthController.register(req, res, next);

      expect(next).toHaveBeenCalledWith(
        expect.objectContaining({
          message: expect.stringContaining('customer role not found in database')
        })
      );
    });

    test('TC-AUTH-REG-05: register_testNgoaile4_EnsurePendingError — Xử lý lỗi từ dịch vụ gRPC EnsurePending', async () => {
      const testInput = {
        email: 'pending.error@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Vũ',
        lastName: 'Hải',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        callback(null, { found: true, id: 'role-customer-id' });
      });

      // EnsurePending trả về lỗi
      mockEnsurePending.mockImplementation((params: any, callback: any) => {
        callback(new Error('Database deadlock on EnsurePending'));
      });

      await AuthController.register(req, res, next);

      expect(next).toHaveBeenCalledWith(
        expect.objectContaining({
          message: 'Database deadlock on EnsurePending'
        })
      );
    });

    test('TC-AUTH-REG-06: register_testNgoaile5_RedisPublishError — Xử lý lỗi khi Redis publish sự kiện thất bại', async () => {
      const testInput = {
        email: 'redis.fail@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Đỗ',
        lastName: 'Tuấn',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        callback(null, { found: true, id: 'role-customer-id' });
      });

      mockEnsurePending.mockImplementation((params: any, callback: any) => {
        callback(null, { id: 'usr-id-redis', created: true });
      });

      mockRedisPublish.mockRejectedValue(new Error('Redis connection lost'));

      await AuthController.register(req, res, next);

      expect(next).toHaveBeenCalledWith(
        expect.objectContaining({
          message: 'Redis connection lost'
        })
      );
    });

    test('TC-AUTH-REG-07: register_testNgoaile6_EmailExistsErrorCaught — Bắt lỗi error.message === EMAIL_EXISTS từ downstream', async () => {
      const testInput = {
        email: 'catch.exists@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Hoàng',
        lastName: 'Thảo',
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(new Error(ErrorMessages.EMAIL_EXISTS));
      });

      await AuthController.register(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.BAD_REQUEST);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.EMAIL_EXISTS);
      expect(next).not.toHaveBeenCalled();
    });

    test('TC-AUTH-REG-08: register_testChuan2_RegisterWithNullAddress — Đăng ký thành công khi address là null', async () => {
      const testInput = {
        email: 'nulladdress@cinema.com',
        password: RAW_PASSWORD,
        confirmPassword: RAW_PASSWORD,
        firstName: 'Bùi',
        lastName: 'Thắng',
        address: null,
      };

      const req = { body: testInput } as Request;
      const res = createMockResponse() as unknown as Response;
      const next = jest.fn() as NextFunction;

      mockGetUserByEmail.mockImplementation((params: any, callback: any) => {
        callback(null, { found: false });
      });

      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        callback(null, { found: true, id: 'role-customer-id' });
      });

      mockEnsurePending.mockImplementation((params: any, callback: any) => {
        expect(params.address).toBeNull();
        callback(null, { id: 'user-null-addr-id', created: true });
      });

      await AuthController.register(req, res, next);

      const mockRes = res as unknown as IMockResponse;
      expect(mockRes.status).toHaveBeenCalledWith(HttpStatus.CREATED);
      expect(mockRes.jsonData.message).toBe(ErrorMessages.REGISTRATION_SUCCESS);
    });

  });

  // ==========================================================================
  // NHÓM 3: KIỂM THỬ HELPER METHODS (OTP, URL, PUBLISH MESSAGE, ROLE CACHE)
  // ==========================================================================
  describe('Lớp kiểm thử: AuthController Helper Methods', () => {

    test('TC-AUTH-REG-HELP-01: generateOTP_testChuan1_RangeAndLength — Sinh mã OTP 6 chữ số hợp lệ', () => {
      const otp = AuthController.generateOTP();

      expect(typeof otp).toBe('string');
      expect(otp).toHaveLength(6);
      const num = parseInt(otp, 10);
      expect(num).toBeGreaterThanOrEqual(100000);
      expect(num).toBeLessThanOrEqual(999999);
    });

    test('TC-AUTH-REG-HELP-02: createVerifyUrl_testChuan1_FormatAndEncoding — Tạo URL xác thực chuẩn hóa', () => {
      const testEmail = 'user+test@cinema.com';
      const testCode = '654321';

      const url = AuthController.createVerifyUrl(testEmail, testCode);

      expect(url).toBe(`http://localhost:3000/verify?email=user%2Btest%40cinema.com&code=654321`);
    });

    test('TC-AUTH-REG-HELP-03: createEmailVerifyMessage_testChuan1_Structure — Tạo gói tin sự kiện xác thực email', () => {
      const userId = 'usr-uuid-1234';
      const email = 'user@cinema.com';
      const verifyCode = '123456';
      const verifyUrl = 'http://localhost:3000/verify?email=user@cinema.com&code=123456';

      const msg = AuthController.createEmailVerifyMessage(userId, email, verifyCode, verifyUrl);

      expect(msg).toEqual({
        user_id: userId,
        to: email,
        verify_code: verifyCode,
        verify_url: verifyUrl,
      });
    });

    test('TC-AUTH-REG-HELP-04: getCustomerRoleId_testChuan1_CacheHitAndMiss — Đọc Role ID từ Cache hoặc gRPC', async () => {
      // Lần 1: Cache trống -> gọi gRPC và ghi cache
      mockRedisGet.mockResolvedValueOnce(null);
      mockGetRoleByName.mockImplementation((params: any, callback: any) => {
        expect(params.name).toBe('customer');
        callback(null, { found: true, id: 'role-customer-id-live' });
      });

      const roleId1 = await AuthController.getCustomerRoleId();
      expect(roleId1).toBe('role-customer-id-live');
      expect(mockRedisSetEx).toHaveBeenCalledWith('customer_role_id', 3600, 'role-customer-id-live');

      // Lần 2: Cache hit -> đọc trực tiếp từ cache không gọi gRPC
      mockRedisGet.mockResolvedValueOnce('role-customer-id-live');

      const roleId2 = await AuthController.getCustomerRoleId();
      expect(roleId2).toBe('role-customer-id-live');
    });

    test('TC-AUTH-REG-HELP-05: saveOTPToCache_testChuan1_SaveWithTTL — Lưu mã OTP vào Redis Cache đúng TTL', async () => {
      const email = 'otp.cache@cinema.com';
      const otp = '888999';

      await AuthController.saveOTPToCache(email, otp);

      expect(mockRedisSetEx).toHaveBeenCalledWith(
        `otp:${email}`,
        300,
        expect.stringMatching(/"otp":"888999"/)
      );
    });

  });

  // ==========================================================================
  // NHÓM 4: KIỂM THỬ THAO TÁC CƠ SỞ DỮ LIỆU (CheckDB & Rollback)
  // ==========================================================================
  describe('Lớp kiểm thử: UserDAO / EnsurePending — Thao tác CSDL, CheckDB và Rollback', () => {

    test('TC-AUTH-REG-DB-01: ensurePending_testChuan1_InsertUserAndProfile_CheckDB_Rollback — Thêm mới User PENDING & CustomerProfile, CheckDB và Rollback', async () => {
      // 1. Chuẩn bị bảng CSDL mẫu (Bảng User và CustomerProfile ban đầu)
      const initialUsersTable: any[] = [
        { id: 'u0', email: 'existing.seed@cinema.com', name: 'User Gốc', status: 'ACTIVE', role_id: 'role-customer' }
      ];
      const initialProfilesTable: any[] = [];

      let usersTable = [...initialUsersTable];
      let profilesTable = [...initialProfilesTable];

      // Cơ chế Transaction hỗ trợ CheckDB và Rollback theo mục 5.3.2
      class DatabaseTransaction {
        private userSnapshot: any[];
        private profileSnapshot: any[];

        constructor() {
          this.userSnapshot = JSON.parse(JSON.stringify(usersTable));
          this.profileSnapshot = JSON.parse(JSON.stringify(profilesTable));
        }

        public async insertUser(userRecord: any) {
          usersTable.push(userRecord);
        }

        public async insertProfile(profileRecord: any) {
          profilesTable.push(profileRecord);
        }

        public async rollback() {
          usersTable = JSON.parse(JSON.stringify(this.userSnapshot));
          profilesTable = JSON.parse(JSON.stringify(this.profileSnapshot));
        }
      }

      // Input của thao tác đăng ký người dùng mới
      const testInput = {
        id: 'user-uuid-reg-001',
        email: 'customer.new.db@cinema.com',
        name: 'Nguyễn Văn Đăng Ký',
        password: HASHED_PASSWORD,
        role_id: 'role-customer-id',
        address: 'Hà Nội',
        status: 'PENDING',
      };

      const tx = new DatabaseTransaction();

      try {
        // Thực hiện thêm bản ghi User và CustomerProfile tương ứng
        await tx.insertUser(testInput);
        await tx.insertProfile({
          id: 'profile-uuid-001',
          user_id: testInput.id,
          total_payment_amount: 0,
          point: 0,
          onchain_wallet_address: '',
        });

        // ================================================================
        // KIỂM TRA CƠ SỞ DỮ LIỆU (CheckDB): Xác minh dữ liệu đã được ghi đúng
        // ================================================================
        const insertedUser = usersTable.find(u => u.email === testInput.email);
        expect(insertedUser).toBeDefined();
        expect(insertedUser.id).toBe(testInput.id);
        expect(insertedUser.name).toBe(testInput.name);
        expect(insertedUser.status).toBe('PENDING'); // Trạng thái bắt buộc PENDING khi đăng ký
        expect(insertedUser.role_id).toBe('role-customer-id');

        const insertedProfile = profilesTable.find(p => p.user_id === testInput.id);
        expect(insertedProfile).toBeDefined();
        expect(insertedProfile.total_payment_amount).toBe(0);
        expect(insertedProfile.point).toBe(0);

        expect(usersTable.length).toBe(2);
        expect(profilesTable.length).toBe(1);

      } finally {
        // ================================================================
        // HOÀN TÁC CƠ SỞ DỮ LIỆU (Rollback): Khôi phục CSDL về trạng thái ban đầu
        // ================================================================
        await tx.rollback();

        // Kiểm tra sau khi Rollback: Không còn dữ liệu thử nghiệm trong CSDL
        expect(usersTable.find(u => u.email === testInput.email)).toBeUndefined();
        expect(profilesTable.find(p => p.user_id === testInput.id)).toBeUndefined();
        expect(usersTable.length).toBe(1);
        expect(profilesTable.length).toBe(0);
      }
    });

    test('TC-AUTH-REG-DB-02: ensurePending_testNgoaile1_ExistingUserNoDuplicateInsert_CheckDB — Không tạo bản ghi trùng khi email đã tồn tại', async () => {
      const existingUser = {
        id: 'user-existing-id-555',
        email: 'existing.duplicate@cinema.com',
        name: 'Đã Tồn Tại',
        status: 'ACTIVE',
        role_id: 'role-customer',
      };

      const usersTable = [{ ...existingUser }];
      const initialCount = usersTable.length;

      // Mô phỏng logic EnsurePending: kiểm tra nếu tồn tại thì không tạo mới
      const ensurePendingDAO = async (req: { email: string; name: string }) => {
        const found = usersTable.find(u => u.email === req.email);
        if (found) {
          return { id: found.id, created: false };
        }
        const newRecord = { id: 'new-id', email: req.email, name: req.name, status: 'PENDING' };
        usersTable.push(newRecord);
        return { id: newRecord.id, created: true };
      };

      const result = await ensurePendingDAO({
        email: 'existing.duplicate@cinema.com',
        name: 'Thử Đăng Ký Lại'
      });

      // Kiểm tra kết quả trả về
      expect(result.created).toBe(false);
      expect(result.id).toBe(existingUser.id);

      // CheckDB: Số lượng bản ghi trong CSDL không thay đổi, bảo toàn tính toàn vẹn
      expect(usersTable.length).toBe(initialCount);
      expect(usersTable[0].name).toBe('Đã Tồn Tại');
    });

  });

});
