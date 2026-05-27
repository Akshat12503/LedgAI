using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace LedgAI.API.Models
{
    [Table("transactions")]
    public class Transaction
    {
        [Key]
        [Column("transaction_id")]
        public int TransactionId { get; set; }

        [Column("user_id")]
        public int UserId { get; set; }

        [Column("category_id")]
        public int? CategoryId { get; set; }

        [Required]
        [Column("amount")]
        public decimal Amount { get; set; }

        [Required]
        [Column("raw_merchant_string")]
        [StringLength(255)]
        public string RawMerchantString { get; set; } = string.Empty;

        [Column("cleaned_merchant_name")]
        [StringLength(100)]
        public string? CleanedMerchantName { get; set; }

        [Column("confidence_score")]
        public decimal? ConfidenceScore { get; set; }

        [Required]
        [Column("transaction_date")]
        public DateTime TransactionDate { get; set; }

        [Column("created_at")]
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        // Entity Framework Relationships
        [ForeignKey("UserId")]
        public User? User { get; set; }
    }
}