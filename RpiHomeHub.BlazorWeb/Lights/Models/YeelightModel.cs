using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Colors.Models;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class YeelightModel : ILightModel
    {
        public string Power { get; set; }

        [JsonProperty("bright")]
        public int Brightness { get; set; }

        [JsonProperty("ct")]
        public int Temperature { get; set; }

        public ColorRGB Color { get; set; }

        public int Hue { get; set; }

        [JsonProperty("sat")]
        public int Saturation { get; set; }
    }
}
