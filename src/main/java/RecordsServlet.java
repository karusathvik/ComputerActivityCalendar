import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.Name;
import javax.naming.NamingException;
import jakarta.servlet.ServletConfig;
import jakarta.servlet.ServletException;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import javax.sql.DataSource;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.SQLException;

@WebServlet(name = "RecordsServlet", urlPatterns = "/api/records")
public class RecordsServlet extends HttpServlet {
    private DataSource dataSource;
    private static ConnectionDB connectionDB;

    @Override
    public void init(ServletConfig config) throws ServletException {
        super.init(config);
        try {
            dataSource = (DataSource) new InitialContext().lookup("java:comp/env/jdbc/trackerdb");
            connectionDB = new ConnectionDB(dataSource);
        } catch (NamingException e) {
            throw new ServletException("Unable to initialize trackerdb datasource", e);
        }
    }

    @Override
    protected void doPost (HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        String user_id = "1";
        String record_time = request.getParameter("record_time");
        String app = request.getParameter("app");
        String title = request.getParameter("title");


        String query = "INSERT INTO activities (user_id, recorded_at, app, title) VALUES (?, ?, ?, ?)";
        String[] params = {user_id, record_time, app, title};
        //getuserid from the current session but for now its hard coded to 1
        try {
            int count = connectionDB.updateFromQuery(query, params);
            if (count != 1) throw new Exception(); //since only one row should been effected
            response.setStatus(201);
            request.getServletContext().log("succesful insertion of the record");
            out.write("{\"success\":\"Added Activity\"}");
        }
        catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            request.getServletContext().log("Unable to add activities", e);
            out.write("{\"error\":\"Unable to add activities\"}");
        }
        finally {
            out.close();
        }
    }
}
