﻿using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Colors.Models;

namespace RpiHomeHub.BlazorWeb.Lights.Models
{
    public class LED_StripModel : ILightModel
    {
        public string Power { get; set; }

        public ColorRGB Color { get; set; }

        public int Brightness { get; set; }

        public string Mode { get; set; }

        [JsonIgnore]
        public string Name { get => "LED strip"; }
    }
}
