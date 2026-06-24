package ui;

import dao.SinhVienDAO;
import entity.SinhVien;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.sql.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.List;

@SuppressWarnings("serial")
public class StudentManagementUI extends JFrame {

    private JTextField txtMaSV, txtHoTen, txtNgaySinh, txtMaLop, txtSearch;
    private JComboBox<String> cbGioiTinh;
    private JButton btnAdd, btnUpdate, btnDelete, btnClear, btnManageGrades, btnSearch, btnRefresh;
    private JTable table;
    private DefaultTableModel model;
    private JLabel lblStatus;

    private SinhVienDAO sinhVienDAO;
    
    private SimpleDateFormat sdf = new SimpleDateFormat("dd-MM-yyyy");

    public StudentManagementUI() {
        setTitle("Hệ Thống Quản Lý Sinh Viên");
        setSize(1050, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        sinhVienDAO = new SinhVienDAO();

        JLabel lblHeader = new JLabel("HỆ THỐNG QUẢN LÝ THÔNG TIN SINH VIÊN", JLabel.CENTER);
        lblHeader.setFont(new Font("Arial", Font.BOLD, 24));
        lblHeader.setOpaque(true);
        lblHeader.setBackground(new Color(0, 102, 153));
        lblHeader.setForeground(Color.WHITE);
        lblHeader.setBorder(new EmptyBorder(15, 0, 15, 0));
        add(lblHeader, BorderLayout.NORTH);

        JPanel pnlMain = new JPanel(new BorderLayout(10, 10));
        pnlMain.setBorder(new EmptyBorder(10, 10, 10, 10));

        // form nhap
        JPanel pnlLeft = new JPanel(new BorderLayout());
        pnlLeft.setPreferredSize(new Dimension(320, 0));

        JPanel pnlForm = new JPanel(new GridBagLayout());
        pnlForm.setBorder(new TitledBorder("Thông Tin Sinh Viên"));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 5, 10, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0; pnlForm.add(new JLabel("Mã SV (*):"), gbc);
        gbc.gridx = 1; gbc.gridy = 0; txtMaSV = new JTextField(15); pnlForm.add(txtMaSV, gbc);

        gbc.gridx = 0; gbc.gridy = 1; pnlForm.add(new JLabel("Họ Tên (*):"), gbc);
        gbc.gridx = 1; gbc.gridy = 1; txtHoTen = new JTextField(15); pnlForm.add(txtHoTen, gbc);

        gbc.gridx = 0; gbc.gridy = 2; pnlForm.add(new JLabel("Ngày Sinh:"), gbc);
        gbc.gridx = 1; gbc.gridy = 2; txtNgaySinh = new JTextField(15); txtNgaySinh.setToolTipText("dd-MM-yyyy"); pnlForm.add(txtNgaySinh, gbc);

        gbc.gridx = 0; gbc.gridy = 3; pnlForm.add(new JLabel("Giới Tính:"), gbc);
        gbc.gridx = 1; gbc.gridy = 3; 
        cbGioiTinh = new JComboBox<>(new String[]{"Nam", "Nữ"}); 
        pnlForm.add(cbGioiTinh, gbc);

        gbc.gridx = 0; gbc.gridy = 4; pnlForm.add(new JLabel("Lớp (*):"), gbc);
        gbc.gridx = 1; gbc.gridy = 4; txtMaLop = new JTextField(15); pnlForm.add(txtMaLop, gbc);

        pnlLeft.add(pnlForm, BorderLayout.CENTER);

        // chuc nang
        JPanel pnlButtons = new JPanel(new GridLayout(2, 2, 5, 5));
        pnlButtons.setBorder(new EmptyBorder(10, 0, 0, 0));

        btnAdd = new JButton("Thêm"); btnAdd.setBackground(new Color(0, 153, 51)); btnAdd.setForeground(Color.WHITE);
        btnUpdate = new JButton("Cập Nhật"); btnUpdate.setBackground(new Color(255, 153, 0)); btnUpdate.setForeground(Color.WHITE);
        btnDelete = new JButton("Xóa"); btnDelete.setBackground(new Color(204, 0, 0)); btnDelete.setForeground(Color.WHITE);
        btnClear = new JButton("Làm Mới"); btnClear.setBackground(Color.GRAY); btnClear.setForeground(Color.WHITE);

        pnlButtons.add(btnAdd);
        pnlButtons.add(btnUpdate);
        pnlButtons.add(btnDelete);
        pnlButtons.add(btnClear);

        JPanel pnlBottomLeft = new JPanel(new BorderLayout());
        pnlBottomLeft.add(pnlButtons, BorderLayout.NORTH);

        btnManageGrades = new JButton("Quản Lý Điểm");
        btnManageGrades.setBackground(new Color(0, 102, 170));
        btnManageGrades.setForeground(Color.WHITE);
        btnManageGrades.setFont(new Font("Arial", Font.BOLD, 14));
        btnManageGrades.setPreferredSize(new Dimension(0, 40));
        
        JPanel pnlGradeBtn = new JPanel(new BorderLayout());
        pnlGradeBtn.setBorder(new EmptyBorder(10, 0, 0, 0));
        pnlGradeBtn.add(btnManageGrades, BorderLayout.CENTER);
        
        pnlBottomLeft.add(pnlGradeBtn, BorderLayout.SOUTH);
        pnlLeft.add(pnlBottomLeft, BorderLayout.SOUTH);
        pnlMain.add(pnlLeft, BorderLayout.WEST);

        // bang
        JPanel pnlRight = new JPanel(new BorderLayout(5, 5));
        pnlRight.setBorder(new TitledBorder("Danh Sách Sinh Viên"));

        JPanel pnlSearch = new JPanel(new FlowLayout(FlowLayout.LEFT));
        pnlSearch.add(new JLabel("Tìm kiếm (Mã/Tên):"));
        txtSearch = new JTextField(20);
        pnlSearch.add(txtSearch);
        btnSearch = new JButton("Tìm Kiếm");
        btnSearch.setBackground(new Color(0, 102, 153)); btnSearch.setForeground(Color.WHITE);
        btnRefresh = new JButton("Tải Lại");
        btnRefresh.setBackground(Color.GRAY); btnRefresh.setForeground(Color.WHITE);
        pnlSearch.add(btnSearch);
        pnlSearch.add(btnRefresh);

        pnlRight.add(pnlSearch, BorderLayout.NORTH);

        String[] cols = {"Mã SV", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp"};
        model = new DefaultTableModel(cols, 0);
        table = new JTable(model);
        table.setRowHeight(25);
        table.getTableHeader().setBackground(new Color(0, 102, 153));
        table.getTableHeader().setForeground(Color.WHITE);
        table.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        
        pnlRight.add(new JScrollPane(table), BorderLayout.CENTER);
        pnlMain.add(pnlRight, BorderLayout.CENTER);

        add(pnlMain, BorderLayout.CENTER);

        lblStatus = new JLabel(" Trạng thái: Đã sẵn sàng");
        lblStatus.setBorder(BorderFactory.createEtchedBorder());
        add(lblStatus, BorderLayout.SOUTH);

        sdf.setLenient(false);

        loadDataToTable();
        addEvents();
    }

    private void loadDataToTable() {
        model.setRowCount(0);
        List<SinhVien> list = sinhVienDAO.getAllSinhVien();
        for (SinhVien sv : list) {
            String dobStr = (sv.getNgaySinh() != null) ? sdf.format(sv.getNgaySinh()) : "";
            model.addRow(new Object[]{sv.getMaSV(), sv.getHoTen(), dobStr, sv.getGioiTinh(), sv.getMaLop()});
        }
    }

    private Date parseDate(String dateStr) throws ParseException {
        if (dateStr == null || dateStr.trim().isEmpty()) {
            return null;
        }
        java.util.Date utilDate = sdf.parse(dateStr);
        return new Date(utilDate.getTime());
    }

    private void addEvents() {
        table.getSelectionModel().addListSelectionListener(e -> {
            int row = table.getSelectedRow();
            if (row >= 0) {
                txtMaSV.setText(model.getValueAt(row, 0).toString());
                txtHoTen.setText(model.getValueAt(row, 1).toString());
                Object dateObj = model.getValueAt(row, 2);
                txtNgaySinh.setText(dateObj != null ? dateObj.toString() : "");
                cbGioiTinh.setSelectedItem(model.getValueAt(row, 3).toString());

                txtMaLop.setText(model.getValueAt(row, 4).toString());
                
                txtMaSV.setEditable(false);
            }
        });

        btnClear.addActionListener(e -> {
            txtMaSV.setEditable(true);
            txtMaSV.setText("");
            txtHoTen.setText("");
            txtNgaySinh.setText("");
            txtMaLop.setText("");
            cbGioiTinh.setSelectedIndex(0);
            table.clearSelection();
            lblStatus.setText(" Trạng thái: Đã làm mới form.");
        });

        btnAdd.addActionListener(e -> {
            try {
                Date dob = parseDate(txtNgaySinh.getText()); 
                String maLop = txtMaLop.getText().trim();
                
                SinhVien sv = new SinhVien(txtMaSV.getText(), txtHoTen.getText(), dob, cbGioiTinh.getSelectedItem().toString(), maLop);
                if (sinhVienDAO.addSinhVien(sv)) {
                    loadDataToTable();
                    btnClear.doClick();
                    lblStatus.setText(" Trạng thái: Thêm sinh viên thành công.");
                } else {
                    JOptionPane.showMessageDialog(this, "Thêm sinh viên thất bại! Vui lòng kiểm tra lại Mã SV hoặc Mã Lớp (phải tồn tại).");
                }
            } catch (ParseException ex) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập ngày sinh đúng định dạng DD-MM-YYYY (VD: 06-10-2007)!");
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi: " + ex.getMessage());
            }
        });

        btnUpdate.addActionListener(e -> {
            try {
                Date dob = parseDate(txtNgaySinh.getText()); 
                String maLop = txtMaLop.getText().trim();
                
                SinhVien sv = new SinhVien(txtMaSV.getText(), txtHoTen.getText(), dob, cbGioiTinh.getSelectedItem().toString(), maLop);
                if (sinhVienDAO.updateSinhVien(sv)) {
                    loadDataToTable();
                    btnClear.doClick();
                    lblStatus.setText(" Trạng thái: Cập nhật thành công.");
                } else {
                    JOptionPane.showMessageDialog(this, "Cập nhật sinh viên thất bại! Kiểm tra lại mã lớp.");
                }
            } catch (ParseException ex) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập ngày sinh đúng định dạng DD-MM-YYYY (VD: 06-10-2007)!");
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(this, "Lỗi: " + ex.getMessage());
            }
        });

        btnDelete.addActionListener(e -> {
            String id = txtMaSV.getText();
            if (!id.isEmpty()) {
                int confirm = JOptionPane.showConfirmDialog(this, "Bạn có chắc chắn muốn xóa sinh viên này?", "Xác nhận", JOptionPane.YES_NO_OPTION);
                if (confirm == JOptionPane.YES_OPTION) {
                    if (sinhVienDAO.deleteSinhVien(id)) {
                        loadDataToTable();
                        btnClear.doClick();
                        lblStatus.setText(" Trạng thái: Đã xóa sinh viên.");
                    } else {
                        JOptionPane.showMessageDialog(this, "Xóa thất bại! Vui lòng xóa điểm của sinh viên này trước.");
                    }
                }
            } else {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn một sinh viên để xóa!");
            }
        });

        btnSearch.addActionListener(e -> {
            String keyword = txtSearch.getText();
            List<SinhVien> list = sinhVienDAO.searchSinhVien(keyword);
            model.setRowCount(0);
            for (SinhVien sv : list) {
                String dobStr = (sv.getNgaySinh() != null) ? sdf.format(sv.getNgaySinh()) : "";
                model.addRow(new Object[]{sv.getMaSV(), sv.getHoTen(), dobStr, sv.getGioiTinh(), sv.getMaLop()});
            }
            lblStatus.setText(" Trạng thái: Tìm thấy " + list.size() + " kết quả.");
        });

        btnRefresh.addActionListener(e -> {
            txtSearch.setText("");
            loadDataToTable();
            lblStatus.setText(" Trạng thái: Đã tải lại danh sách.");
        });

        btnManageGrades.addActionListener(e -> {
            int row = table.getSelectedRow();
            if (row < 0) {
                JOptionPane.showMessageDialog(this, "Vui lòng chọn một sinh viên trên bảng để quản lý điểm!");
                return;
            }
            String maSV = model.getValueAt(row, 0).toString();
            String hoTen = model.getValueAt(row, 1).toString();
            ManageGradesDialog dialog = new ManageGradesDialog(this, maSV, hoTen);
            dialog.setVisible(true);
        });
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new StudentManagementUI().setVisible(true);
        });
    }
}