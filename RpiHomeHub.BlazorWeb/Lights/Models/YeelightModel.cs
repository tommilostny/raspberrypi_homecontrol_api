using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Core;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class YeelightModel : ILightModel
    {
        public string Power { get; set; }

        [JsonProperty("bright")]
        public int Brightness { get; set; }

        [JsonProperty("ct")]
        public int Temperature { get; set; }

        public int RGB { get; set; }

        [JsonIgnore]
        public ColorRGB Color
        {
            get => new()
            {
                Blue = RGB & 0x0000FF,
                Green = (RGB & 0x00FF00) >> 8,
                Red = (RGB & 0xFF0000) >> 16
            };
        }

        public int Hue { get; set; }

        [JsonProperty("sat")]
        public int Saturation { get; set; }
    }
}
