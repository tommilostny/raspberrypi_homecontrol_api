using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Lights.Models;
using System.Net.Http;
using System.Threading.Tasks;
using System.Collections.Generic;
using RpiHomeHub.BlazorWeb.Colors.Models;

namespace RpiHomeHub.BlazorWeb.Lights.Services
{
    public class AllLightsService
    {
        private readonly HttpClient _httpClient;

        public AllLightsService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<List<ILightModel>> GetStatusAsync()
        {
            var lampTask = _httpClient.GetAsync("lamp");
            var yeelightTask = _httpClient.GetAsync("yeelight");
            var stripTask = _httpClient.GetAsync("ledstrip");

            var statuses = new List<ILightModel>();
            await Task.WhenAll(lampTask, yeelightTask, stripTask);

            statuses.Add(JsonConvert.DeserializeObject<LampModel>(await lampTask.Result.Content.ReadAsStringAsync()));
            statuses.Add(JsonConvert.DeserializeObject<YeelightModel>(await yeelightTask.Result.Content.ReadAsStringAsync()));
            statuses.Add(JsonConvert.DeserializeObject<LED_StripModel>(await stripTask.Result.Content.ReadAsStringAsync()));
            return statuses;
        }

        public async Task ToggleAsync(List<ILightModel> lights)
        {
            await _httpClient.GetAsync("lights/toggle");
            lights.ForEach(l => l.Power = l.Power == "on" ? "off" : "on");
        }

        public async Task TurnOffAsync(List<ILightModel> lights)
        {
            await _httpClient.GetAsync("lights/off");
            lights.ForEach(l => l.Power = "off");
        }

        public async Task TurnOnAsync(List<ILightModel> lights)
        {
            await _httpClient.GetAsync("lights/on");
            lights.ForEach(l => l.Power = "on");
        }

        public async Task SetColorAsync(int red, int green, int blue, List<ILightModel> lights)
        {
            await _httpClient.GetAsync($"lights/{red}/{green}/{blue}");
            lights.ForEach(l => l.Color.Red = red);
            lights.ForEach(l =>  l.Color.Green = green);
            lights.ForEach(l => l.Color.Blue = blue);
        }

        public async Task SetBrightnessAsync(int brightness, List<ILightModel> lights)
        {
            await _httpClient.GetAsync($"lights/{brightness}");
            lights.ForEach(l => l.Brightness = brightness);
        }

        public async Task ColorCycle(string direction, List<ILightModel> lights)
        {
            var response = await _httpClient.GetAsync($"lights/color_cycle/{direction}");
            var content = await response.Content.ReadAsStringAsync();
            var newColor = JsonConvert.DeserializeObject<ColorRGB>(content);

            lights.ForEach(l => l.Color.Red = newColor.Red);
            lights.ForEach(l => l.Color.Green = newColor.Green);
            lights.ForEach(l => l.Color.Blue = newColor.Blue);
        }
    }
}
