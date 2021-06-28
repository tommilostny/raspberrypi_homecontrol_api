using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class LED_StripService : LightServiceBase, ILightService
    {
        public LED_StripService(HttpClient httpClient) : base(httpClient)
        {
        }

        public async Task<ILightModel> GetStatus()
        {
            var response = await _httpClient.GetAsync("ledstrip");
            var content = await response.Content.ReadAsStringAsync();

            return JsonConvert.DeserializeObject<LED_StripModel>(content);
        }

        public async Task<ILightModel> Toggle()
        {
            await _httpClient.GetAsync("ledstrip/toggle");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOff()
        {
            await _httpClient.GetAsync("ledstrip/off");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOn()
        {
            await _httpClient.GetAsync("ledstrip/on");
            return await GetStatus();
        }

        public async Task<ILightModel> SetColor(int red, int green, int blue)
        {
            await _httpClient.GetAsync($"ledstrip/{red}/{green}/{blue}");
            return await GetStatus();
        }

        public async Task<ILightModel> SetBrightness(int brightness)
        {
            await _httpClient.GetAsync($"ledstrip/{brightness}");
            return await GetStatus();
        }
    }
}
