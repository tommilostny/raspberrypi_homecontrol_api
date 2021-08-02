using Microsoft.AspNetCore.Components;
using RpiHomeHub.BlazorWeb.Lights.Services;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace RpiHomeHub.BlazorWeb.Lights.Components
{
    public partial class AllLightsControlsComponent : ComponentBase
    {
        [Inject]
        public AllLightsService LightsService { get; set; }

        private List<ILightModel> Lights { get; } = new();

        private int LowerLimit
        {
            get => _lowerLimit;
            set => _lowerLimit = value < _upperLimit ? value : _upperLimit - 1;
        }
        private int _lowerLimit = 40;
        
        private int UpperLimit
        {
            get => _upperLimit;
            set => _upperLimit = value > _lowerLimit ? value : _lowerLimit + 1;
        }
        private int _upperLimit = 100;

        protected override async Task OnInitializedAsync()
        {
            await Load();
            await base.OnInitializedAsync();
        }

        private async Task Load()
        {
            Lights.Clear();
            Lights.AddRange(await LightsService.GetStatusAsync());
        }

        private async Task Toggle() => await LightsService.ToggleAsync(Lights);

        private async Task TurnOn() => await LightsService.TurnOnAsync(Lights);

        private async Task TurnOff() => await LightsService.TurnOffAsync(Lights);

        private async Task NextColor() => await LightsService.ColorCycle("next", Lights);

        private async Task PreviousColor() => await LightsService.ColorCycle("previous", Lights);

        private async Task BrightnessCycle() => await LightsService.BrightnessCycle(Lights, LowerLimit, UpperLimit);
    }
}
