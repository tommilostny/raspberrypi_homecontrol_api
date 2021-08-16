using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record WindModel
    {
        public float Speed { get; set; }

        [JsonProperty("deg")]
        public float Angle { get; set; }

        [JsonIgnore]
        public string Direction { get => Angle switch
        {
            0 => "East",
            90 => "North",
            180 => "West",
            270 => "South",
            > 0 and < 90 => "North-East",
            > 90 and < 180 => "North-West",
            > 180 and < 270 => "South-West",
            > 270 and < 360 => "South-East",
            _ => "Unknown"
        }; }
    }
}
