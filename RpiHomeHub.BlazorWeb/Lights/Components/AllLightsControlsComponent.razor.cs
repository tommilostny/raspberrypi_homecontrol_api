using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Components
{
    public partial class AllLightsControlsComponent : ComponentBase
    {
        public List<ILightModel> Lights { get; set; } = new();

        [Inject]
        public AllLightsService LightsService { get; set; }

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        private async Task Load()
        {
            Lights.Clear();
            var result = await LightsService.GetStatusAsync();
            Lights.AddRange(result);
        }

        private async Task Toggle() => await LightsService.ToggleAsync(Lights);

        private async Task TurnOn() => await LightsService.TurnOnAsync(Lights);

        private async Task TurnOff() => await LightsService.TurnOffAsync(Lights);

        private async Task NextColor() => await LightsService.ColorCycle("next", Lights);

        private async Task PreviousColor() => await LightsService.ColorCycle("previous", Lights);

        //private async Task SetBrightness() => await LightsService.SetBrightnessAsync(Light.Brightness, Light);
    }
}
