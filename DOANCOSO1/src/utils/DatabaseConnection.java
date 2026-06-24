package utils;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {


    private static final String URL = "jdbc:sqlserver://LAPTOP-2SSGG9O3\\MSSQLSERVER2025;"
            + "databaseName=DOANCOSO1;"
            + "encrypt=true;"
            + "trustServerCertificate=true;";
    private static final String USER = "sa";
    private static final String PASSWORD = "1";

    public static Connection getConnection() {
        Connection conn = null;
        try {
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");

            conn = DriverManager.getConnection(URL, USER, PASSWORD);
        } catch (ClassNotFoundException e) {
            System.err.println("LỖI: Không tìm thấy Driver SQL Server! Hãy kiểm tra lại thư viện mssql-jdbc.");
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println("LỖI: Kết nối đến SQL Server thất bại! Kiểm tra lại URL, tài khoản hoặc mật khẩu.");
            e.printStackTrace();
        }
        return conn;
    }

    public static void closeConnection(Connection conn) {
        if (conn != null) {
            try {
                conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Đang tiến hành test kết nối tới CSDL...");
        Connection testConn = DatabaseConnection.getConnection();
        
        if (testConn != null) {
            System.out.println("=========================================");
            System.out.println(" CHÚC MỪNG: KẾT NỐI DATABASE THÀNH CÔNG! ");
            System.out.println("=========================================");
            
            DatabaseConnection.closeConnection(testConn);
        } else {
            System.err.println("=========================================");
            System.err.println(" THẤT BẠI: Vui lòng kiểm tra lại SQL Server! ");
            System.err.println("=========================================");
        }
    }
}