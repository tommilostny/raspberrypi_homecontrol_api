using Microsoft.AspNetCore.Components;
using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Weather.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Weather
{
    public partial class WeatherComponent : ComponentBase
    {
        [Inject]
        public HttpClient Http { get; set; }

        private WeatherModel Weather { get; set; }

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        public async Task Load()
        {
            var response = await Http.GetAsync("weather");
            var content = await response.Content.ReadAsStringAsync();
            Weather = JsonConvert.DeserializeObject<WeatherModel>(content);
        }
    }
}
