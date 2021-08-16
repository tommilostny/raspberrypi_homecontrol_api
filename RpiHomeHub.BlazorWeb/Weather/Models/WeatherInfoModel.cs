using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record WeatherInfoModel
    {
        public int Id { get; set; }

        [JsonProperty("main")]
        public string Title { get; set; }

        public string Description { get; set; }

        public string Icon { get; set; }

        [JsonIgnore]
        public string IconLink { get => $"https://openweathermap.org/img/wn/{Icon}.png"; }
    }
}
