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

        public async Task<int> SetBrightnessAsync(int brightness)
        {
            await _httpClient.GetAsync($"{_endpointBase}/{brightness}");
            return brightness;
        }

        public async Task<ColorRGB> SetColorAsync(ColorRGB color)
        {
            await _httpClient.GetAsync($"{_endpointBase}/{color.Red}/{color.Green}/{color.Blue}");
            return color;
        }

        public async Task<TLightModel> ToggleAsync()
        {
            await _httpClient.GetAsync($"{_endpointBase}/toggle");
            return await GetStatusAsync();
        }

        public async Task<TLightModel> TurnOffAsync()
        {
            await _httpClient.GetAsync($"{_endpointBase}/off");
            return await GetStatusAsync();
        }

        public async Task<TLightModel> TurnOnAsync()
        {
            await _httpClient.GetAsync($"{_endpointBase}/on");
            return await GetStatusAsync();
        }
    }
}