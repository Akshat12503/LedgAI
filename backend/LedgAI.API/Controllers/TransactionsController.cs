using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using LedgAI.API.Data;
using LedgAI.API.Models;

namespace LedgAI.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TransactionsController : ControllerBase
    {
        private readonly AppDbContext _context;

        // Inject our database context through the constructor
        public TransactionsController(AppDbContext context)
        {
            _context = context;
        }

        // GET: api/transactions
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Transaction>>> GetTransactions()
        {
            try
            {
                // Fetch all records from the database asynchronously
                var transactions = await _context.Transactions.ToListAsync();
                return Ok(transactions);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}