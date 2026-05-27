using Microsoft.EntityFrameworkCore;
using LedgAI.API.Data;

var builder = WebApplication.CreateBuilder(args);

// 1. Fetch our Connection String from appsettings.json
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// 2. Register the AppDbContext using the Npgsql PostgreSQL Driver
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

// 3. Define CORS Policy to explicitly trust and allow your Angular client (Port 4200)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAngularClient",
        policy => policy.WithOrigins("http://localhost:4200")
                        .AllowAnyMethod()
                        .AllowAnyHeader());
});

// Add standard Web API services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
// builder.Services.AddSwaggerGen(); // Commented out to bypass missing template dependencies

var app = builder.Build();

// 4. Activate the CORS routing rule (CRITICAL: Must be called before MapControllers)
app.UseCors("AllowAngularClient");

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();