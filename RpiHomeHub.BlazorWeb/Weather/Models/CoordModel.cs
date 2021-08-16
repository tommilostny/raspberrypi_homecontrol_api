using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record CoordModel
    {
        [JsonProperty("lon")]
        public float Longitude { get; set; }

        [JsonProperty("lat")]
        public float Latitude { get; set; }
    }
}
