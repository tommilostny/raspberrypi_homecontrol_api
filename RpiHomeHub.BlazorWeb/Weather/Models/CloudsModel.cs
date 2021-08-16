using Newtonsoft.Json;

namespace RpiHomeHub.BlazorWeb.Weather.Models
{
    public record CloudsModel
    {
        [JsonProperty("all")]
        public float Percentage { get; set; }
    }
}
