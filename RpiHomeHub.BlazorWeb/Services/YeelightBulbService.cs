using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Services
{
    public class YeelightBulbService
    {
        private readonly HttpClient _httpClient;

        public YeelightBulbService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<YeelightBulbModel> GetStatus()
        {
            var response = await _httpClient.GetAsync("yeelight");
            var content = await response.Content.ReadAsStringAsync();

            var bulb = JsonConvert.DeserializeObject<YeelightBulbModel>(content);
            bulb.Color = DecodeColor(bulb.RGB);
            return bulb;
        }

        public async Task<YeelightBulbModel> Toggle()
        {
            await _httpClient.GetAsync("lights/power/toggle");
            return await GetStatus();
        }

        private static ColorRGB DecodeColor(int rgb) => new ColorRGB
        {
            Blue = rgb & 0x0000FF,
            Green = (rgb & 0x00FF00) >> 8,
            Red = (rgb & 0xFF0000) >> 16
        };
    }
}
