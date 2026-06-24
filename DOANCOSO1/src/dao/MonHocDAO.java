package dao;

import entity.MonHoc;
import utils.DatabaseConnection;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class MonHocDAO {

    public List<MonHoc> getAllMonHoc() {
        List<MonHoc> list = new ArrayList<>();
        String sql = "SELECT * FROM MONHOC";
        try (Connection conn = DatabaseConnection.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                MonHoc mh = new MonHoc(
                    rs.getString("MaMon"),
                    rs.getString("TenMon"),
                    rs.getInt("SoTinChi"),
                    rs.getInt("LoaiMon"),
                    rs.getString("MaKhoa")
                );
                list.add(mh);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return list;
    }
}