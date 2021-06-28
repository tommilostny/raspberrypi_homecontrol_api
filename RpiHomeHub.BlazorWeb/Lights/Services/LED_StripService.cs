using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class LED_StripService : LightServiceBase<LED_StripModel>
    {
        public LED_StripService(HttpClient httpClient) : base(httpClient, "ledstrip")
        {
        }
    }
}
