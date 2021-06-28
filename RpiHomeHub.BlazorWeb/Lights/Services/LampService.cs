using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class LampService : LightServiceBase, ILightService
    {
        public LampService(HttpClient httpClient) : base(httpClient)
        {
        }

        public async Task<ILightModel> GetStatus()
        {
            var response = await _httpClient.GetAsync("lamp");
            var content = await response.Content.ReadAsStringAsync();

            return JsonConvert.DeserializeObject<LampModel>(content);
        }

        public async Task<ILightModel> Toggle()
        {
            await _httpClient.GetAsync("lamp/toggle");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOff()
        {
            await _httpClient.GetAsync("lamp/off");
            return await GetStatus();
        }

        public async Task<ILightModel> TurnOn()
        {
            await _httpClient.GetAsync("lamp/on");
            return await GetStatus();
        }

        public async Task<ILightModel> SetColor(int red, int green, int blue)
        {
            await _httpClient.GetAsync($"lamp/{red}/{green}/{blue}");
            return await GetStatus();
        }

        public async Task<ILightModel> SetBrightness(int brightness)
        {
            await _httpClient.GetAsync($"lamp/{brightness}");
            return await GetStatus();
        }
    }
}
