import java.sql.*;

public class OracleCon {
    public static void main(String args[]) {
        try {
            // step1 parse Input
            String oracleUrl = args[0];
            String username = args[1];
            String password = args[2];
            String sql = args[3];


            // step1 load the driver class
            Class.forName("oracle.jdbc.driver.OracleDriver");

            // step2 create  the connection object
            Connection con = DriverManager.getConnection(oracleUrl, username, password);

            // step3 create the statement object
            Statement stmt = con.createStatement();

            // step4 execute query
            ResultSet rs = stmt.executeQuery(sql);

            String resutlt = ResultSetConverter.convert(rs);

            System.out.println(resutlt);

            // step5 close the connection object
            con.close();
        } catch (Exception e) {
            System.out.println(e);
        }

    }
}

class ResultSetConverter {
	
	public static String dealQuot(String orgString) {
		char[] array = orgString.toCharArray();
		int length = orgString.length();
		String result = "";
		for (int i=0; i<length; i++)
		{
			if (array[i] == '\"') {
				result += '\\';
			}				
			result += array[i];
		}
		return "\"" + result + "\"";
	}
	
	
    public static String convert(ResultSet rs) throws SQLException {
        ResultSetMetaData rsmd = rs.getMetaData();
        int numColumns = rsmd.getColumnCount();
		String result = "[";
        while (rs.next()) {
			String row = "{";
            for (int i = 1; i < numColumns + 1; i++) {
                String column_name = rsmd.getColumnName(i);
                Object ob = rs.getObject(column_name);
				String value = ob == null? "None": dealQuot(ob.toString());

				if (i == numColumns) {
					row += dealQuot(column_name) + ": " + value;
				} else {
					row += dealQuot(column_name) + ": " + value + ", ";
				}
            }
			row += "}";
			
			result += row + ", ";
        }
		if (result.length() > 1) {
			result = result.substring(0, result.length() -2 );
		}
		return result + "]";
    }
}
