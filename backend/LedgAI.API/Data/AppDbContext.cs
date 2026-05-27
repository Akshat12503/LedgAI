using Microsoft.EntityFrameworkCore;
using LedgAI.API.Models;

namespace LedgAI.API.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        // Define our DbSets (These map directly to your PostgreSQL tables)
        public DbSet<User> Users { get; set; } = null!;
        public DbSet<Transaction> Transactions { get; set; } = null!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Let Entity Framework know that the database handles generating the primary key IDs natively via SERIAL
            modelBuilder.Entity<User>()
                .Property(u => u.UserId)
                .ValueGeneratedOnAdd();

            modelBuilder.Entity<Transaction>()
                .Property(t => t.TransactionId)
                .ValueGeneratedOnAdd();
        }
    }
}