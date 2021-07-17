using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class YeelightService : LightServiceBase<YeelightModel>
    {
        public YeelightService(HttpClient httpClient) : base(httpClient, "yeelight")
        {
        }

        public async Task SetTemperatureAsync(int temperature, YeelightModel yeelight)
        {
            await _httpClient.GetAsync($"{_endpointBase}/temperature/{temperature}");
            yeelight.Temperature = temperature;
        }

        public async Task SetHueSaturationAsync(int hue, int saturation, YeelightModel yeelight)
        {
            await _httpClient.GetAsync($"{_endpointBase}/hs/{hue}/{saturation}");
            yeelight.Hue = hue;
            yeelight.Saturation = saturation;
        }
    }
}
