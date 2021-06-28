using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class YeelightService : LightServiceBase, ILightService
    {
        public YeelightService(HttpClient httpClient) : base(httpClient)
        {
        }

        public async Task<ILightModel> GetStatus()
        {
            var response = await _httpClient.GetAsync("yeelight");
            var content = await response.Content.ReadAsStringAsync();

            return JsonConvert.DeserializeObject<YeelightModel>(content);
        }

        public async Task<ILightModel> Toggle()
        {
            await _httpClient.GetAsync("yeelight/toggle");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOff()
        {
            await _httpClient.GetAsync("yeelight/off");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOn()
        {
            await _httpClient.GetAsync("yeelight/on");
            return await GetStatus();
        }

        public async Task<ILightModel> SetColor(int red, int green, int blue)
        {
            await _httpClient.GetAsync($"yeelight/{red}/{green}/{blue}");
            return await GetStatus();
        }

        public async Task<ILightModel> SetBrightness(int brightness)
        {
            await _httpClient.GetAsync($"yeelight/{brightness}");
            return await GetStatus();
        }
    }
}
