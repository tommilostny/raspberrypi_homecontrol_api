using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Temperature
{
    public class TemperatureModel
    {
        [JsonProperty("tempC")]
        public float Celsius { get; set; }

        [JsonProperty("tempF")]
        public float Fahrenheit { get; set; }

        [JsonProperty("tempK")]
        public float Kelvin { get; set; }

        public float ThresholdDay { get; set; }

        public float ThresholdNight { get; set; }

        public float FanThreshold { get; set; }
    }
}
