using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record WeatherModel
    {
        public CoordModel Coord { get; set; }

        [JsonProperty("weather")]
        public WeatherInfoModel[] WeatherInfos { get; set; }

        [JsonProperty("main")]
        public MainWeatherModel MainWeather { get; set; }

        public float Visibility { get; set; }

        public WindModel Wind { get; set; }

        public CloudsModel Clouds { get; set; }

        [JsonProperty("dt")]
        public long DataCalculationTime { get; set; }

        public long Id { get; set; }

        public string Name { get; set; }
    }
}
