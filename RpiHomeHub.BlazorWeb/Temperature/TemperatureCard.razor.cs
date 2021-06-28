using Microsoft.AspNetCore.Components;
using Newtonsoft.Json;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Temperature
{
    public partial class TemperatureCard : ComponentBase
    {
        private const string nightString = "night";
        private const string dayString = "day";
        private const string fanString = "fan";

        [Inject]
        private HttpClient HttpClient { get; set; }

        private TemperatureModel Temperature { get; set; }

        [Parameter]
        public bool ShowThresholdSetting { get; set; } = true;

        private async Task GetTemperature()
        {
            Temperature = null;
            var response = await HttpClient.GetAsync("temperature");
            var content = await response.Content.ReadAsStringAsync();
            Temperature = JsonConvert.DeserializeObject<TemperatureModel>(content);
        }

        private async Task SetTempThreshold(string period)
        {
            float newThreshold = period switch
            {
                "day" => Temperature.ThresholdDay,
                "night" => Temperature.ThresholdNight,
                "fan" => Temperature.FanThreshold,
                _ => throw new InvalidOperationException()
            };
            await HttpClient.GetAsync($"temp_threshold/{period}/{string.Format("{0:N3}", newThreshold)}");
        }

        protected override async Task OnInitializedAsync()
        {
            await GetTemperature();
            await base.OnInitializedAsync();
        }
    }
}
