using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class LampService : LightServiceBase<LampModel>
    {
        public LampService(HttpClient httpClient) : base(httpClient, "lamp")
        {
        }
    }
}
