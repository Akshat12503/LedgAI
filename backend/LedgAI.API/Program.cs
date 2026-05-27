using Microsoft.EntityFrameworkCore;
using LedgAI.API.Data;

var builder = WebApplication.CreateBuilder(args);

// 1. Fetch our Connection String from appsettings.json
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

// 2. Register the AppDbContext using the Npgsql PostgreSQL Driver
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

// Add standard Web API services
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
// builder.Services.AddSwaggerGen(); // Commented out to bypass missing template dependencies

var app = builder.Build();

// Configure the HTTP request pipeline.
// if (app.Environment.IsDevelopment())
// {
//     app.UseSwagger();   // Commented out
//     app.UseSwaggerUI(); // Commented out
// }

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();