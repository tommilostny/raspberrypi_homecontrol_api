using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record MainWeatherModel
    {
        [JsonProperty("temp")]
        public float Temperature { get; set; }

        [JsonProperty("feels_like")]
        public float FeelsLike { get; set; }

        [JsonProperty("temp_min")]
        public float MinimalTemperature { get; set; }

        [JsonProperty("temp_max")]
        public float MaximalTemperature { get; set; }

        public float Pressure { get; set; }

        public float Humidity { get; set; }
    }
}
