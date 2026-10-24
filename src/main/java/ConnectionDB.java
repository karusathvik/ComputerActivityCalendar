import java.sql.*;
import com.google.gson.JsonArray;
import  com.google.gson.JsonObject;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;

//Note: we sitll have to combine the elements inside the json array, so we avoid collisions if lets say two different tables have the same column_ame
//but this is more messing around with json than querying the DB
public class ConnectionDB {
    private static DataSource dataSource;
    public int status = 0; //0 good, 1 bad
    public ConnectionDB(DataSource dataSource)  {
        this.dataSource = dataSource;
    }

    public JsonArray getJsonArrayFromQuery(String query, String[] params ) throws  SQLException{
        //query is in sql
        JsonArray jsonArray = new JsonArray();

        try (Connection connection = dataSource.getConnection()) {
            PreparedStatement statement = connection.prepareStatement(query);

            for (int i = 1; i <= params.length; ++i)
                statement.setString(i,params[i-1]);
            ResultSet result = statement.executeQuery();
            ResultSetMetaData metadata = result.getMetaData();

            while (result.next()) {
                JsonObject jsonObject = new JsonObject();
                for (int i = 1; i <= metadata.getColumnCount(); i++) {
                    jsonObject.addProperty(metadata.getColumnLabel(i), result.getString(i));
                }
                jsonArray.add(jsonObject);
            }

        }
        return jsonArray;

    }

    //for post methods
    public int updateFromQuery(String query, String[] params) throws SQLException {
        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(query)) {
            for (int i = 0; i < params.length; ++i)
                statement.setString(i + 1, params[i]);
            return statement.executeUpdate();
        }
    }


    public int getStatus() {
        return status;
    }

    public void resetStatus() {
        status = 0; //set to good again
    }


}
