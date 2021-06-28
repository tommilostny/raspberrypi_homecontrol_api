using System.Net.Http;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public abstract class LightServiceBase
    {
        protected readonly HttpClient _httpClient;

        public LightServiceBase(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }
    }
}