using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Colors.Models;
using RpiHomeHub.BlazorWeb.Colors.Services;
using RpiHomeHub.BlazorWeb.Lights;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Colors.Components
{
    public partial class ColorPicker<TLightModel> where TLightModel : class, ILightModel, new()
    {
        [Parameter]
        public LightServiceBase<TLightModel> LightService { get; set; }

        [Parameter]
        public EventCallback RefreshEvent { get; set; }

        [Parameter]
        public TLightModel Light { get; set; }

        [Parameter]
        public bool ShowLabels { get; set; } = true;

        [Inject]
        private ColorDbService ColorDbService { get; set; }

        private List<ColorModel> Colors { get; set; }

        private ColorRGB CustomColor { get; set; }

        private static string SetButtonColor(ColorRGB color) => $"background-color: rgb({color.Red},{color.Green},{color.Blue});";

        private async Task SendColor(ColorRGB color)
        {
            await LightService.SetColorAsync(color, Light);
            await RefreshEvent.InvokeAsync();
        }

        protected override async Task OnInitializedAsync()
        {
            Colors = await ColorDbService.GetColorDb();

            CustomColor = new ColorRGB
            {
                Red = Light.Color.Red,
                Green = Light.Color.Green,
                Blue = Light.Color.Blue
            };
            await base.OnInitializedAsync();
        }
    }
}
