using Microsoft.AspNetCore.Components;
using Newtonsoft.Json;
using RpiHomeHub.BlazorWeb.Colors;
using RpiHomeHub.BlazorWeb.Lights;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Colors
{
    public partial class ColorPicker<TLightModel> where TLightModel : class, ILightModel, new()
    {
        [Parameter]
        public LightServiceBase<TLightModel> LightService { get; set; }

        [Parameter]
        public EventCallback RefreshEvent { get; set; }

        [Parameter]
        public ColorRGB Color { get; set; }

        [Parameter]
        public bool ShowLabels { get; set; } = true;

        [Inject]
        private ColorDbService ColorDbService { get; set; }

        private List<ColorModel> Colors { get; set; }

        private ColorRGB CustomColor { get; set; }

        private static string SetButtonColor(ColorRGB color) => $"background-color: rgb({color.Red},{color.Green},{color.Blue});";

        private async Task SendColor(ColorRGB color)
        {
            Color = await LightService.SetColorAsync(color);
            await RefreshEvent.InvokeAsync();
        }

        protected override async Task OnInitializedAsync()
        {
            Colors = await ColorDbService.GetColorDb();

            CustomColor = new ColorRGB
            {
                Red = Color.Red,
                Green = Color.Green,
                Blue = Color.Blue
            };
            await base.OnInitializedAsync();
        }
    }
}
