import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import javax.naming.Context;
import javax.naming.InitialContext;
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

@WebServlet(name = "DisplayServlet", urlPatterns = "/api/display")
public class DisplayServlet extends HttpServlet {
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
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException{
        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        String user_id = request.getParameter("user_id"); //prolly should store this in a session or something so that way users cant access others
        String date = request.getParameter("curr_date"); //this should be in the format YYYY-MM-DD

        LocalDate day;
        try {
            if (user_id == null || Integer.parseInt(user_id) <= 0 || date == null) {
                throw new IllegalArgumentException("Missing or invalid parameters");
            }
            day = LocalDate.parse(date);
        } catch (IllegalArgumentException | DateTimeParseException e) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            out.write("{\"error\":\"Provide a positive user_id and curr_date in YYYY-MM-DD format\"}");
            out.close();
            return;
        }
        String sdate = day + " 00:00:00";
        String edate = day.plusDays(1) + " 00:00:00";
        try {
            String query = "SELECT recorded_at, app, title FROM activities WHERE user_id = ? AND recorded_at >= ? AND recorded_at < ?  ORDER BY recorded_at";
            String[] params = {user_id, sdate, edate};
            JsonArray result = connectionDB.getJsonArrayFromQuery(query, params);
            out.write(result.toString());
            response.setStatus(200);
            request.getServletContext().log(result.toString());
        }
        catch (Exception e) {
            request.getServletContext().log("Unable to retrieve activities", e);
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            out.write("{\"error\":\"Unable to retrieve activities\"}");
        }
        finally {
            out.close();
        }
    }



}
