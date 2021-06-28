using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class YeelightService : LightServiceBase<YeelightModel>
    {
        public YeelightService(HttpClient httpClient) : base(httpClient, "yeelight")
        {
        }
    }
}
