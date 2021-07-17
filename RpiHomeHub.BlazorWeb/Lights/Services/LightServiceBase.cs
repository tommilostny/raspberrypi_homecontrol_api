using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Colors.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class LightServiceBase<TLightModel> : ILightService<TLightModel>
        where TLightModel : class, ILightModel, new()
    {
        protected readonly HttpClient _httpClient;

        protected readonly string _endpointBase;

        public LightServiceBase(HttpClient httpClient, string endpointBase)
        {
            _httpClient = httpClient;
            _endpointBase = endpointBase;
        }

        public async Task<TLightModel> GetStatusAsync()
        {
            var response = await _httpClient.GetAsync(_endpointBase);
            var content = await response.Content.ReadAsStringAsync();
            
            return JsonConvert.DeserializeObject<TLightModel>(content);
        }

        public async Task SetBrightnessAsync(int brightness, TLightModel light)
        {
            await _httpClient.GetAsync($"{_endpointBase}/{brightness}");
            light.Brightness = brightness;
        }

        public async Task SetColorAsync(ColorRGB color, TLightModel light)
        {
            await _httpClient.GetAsync($"{_endpointBase}/{color.Red}/{color.Green}/{color.Blue}");
            light.Color.Red = color.Red;
            light.Color.Green = color.Green;
            light.Color.Blue = color.Blue;
        }

        public async Task ToggleAsync(TLightModel light)
        {
            await _httpClient.GetAsync($"{_endpointBase}/toggle");
            light.Power = light.Power == "on" ? "off" : "on";
        }

        public async Task TurnOffAsync(TLightModel light)
        {
            await _httpClient.GetAsync($"{_endpointBase}/off");
            light.Power = "off";
        }

        public async Task TurnOnAsync(TLightModel light)
        {
            await _httpClient.GetAsync($"{_endpointBase}/on");
            light.Power = "on";
        }
    }
}
