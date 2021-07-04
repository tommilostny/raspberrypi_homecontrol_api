using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Colors.Models;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class LED_StripModel : ILightModel
    {
        public string Power { get; set; }

        [JsonProperty("rgbValue")]
        public ColorRGB Color { get; set; }

        public int White { get; set; }

        public int Brightness { get; set; }
    }
}
